from celery import shared_task
from django.conf import settings
import requests
from twilio.rest import Client
from .models import Report, AuditLog
from apps.authorities.models import Authority
from math import radians, sin, cos, sqrt, atan2
import logging



API_KEY = settings.LOCATIONIQ_API_KEY
TWILIO_CLIENT = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
logger = logging.getLogger(__name__)


def geocode_location(location_name):
    url = "https://us1.locationiq.com/v1/search.php"
    params = {
        "key": API_KEY,
        "q": location_name,
        "format": "json",
        "limit": 1,
        "countrycodes": "KE"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        logger.error(f"Geocoding failed for {location_name}: {e}")
        return None

    if isinstance(data, list) and data:
        return float(data[0]["lat"]), float(data[0]["lon"])
    
    logger.warning(f"No geocoding results for {location_name}")
    return None


def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def get_nearest_police_station(lat, lon):
    nearest = None
    min_dist = float('inf')

    for authority_id, station_lat, station_lon in Authority.objects.values_list("id", "latitude", "longitude"):
        dist = haversine(lat, lon, station_lat, station_lon)
        if dist < min_dist:
            nearest = authority_id
            min_dist = dist

    return Authority.objects.get(pk=nearest) if nearest else None


def send_twilio_sms(report, phone, authority_name, action):
    try:
        authority_instance = Authority.objects.filter(name=authority_name).first()
        if not authority_instance:
            logger.warning(f"Authority '{authority_name}' not found.")
            return
        # Decrypt the report description before sending SMS
        decrypted_description = report.get_decrypted_description()

        msg = (
                f"New report received!\n"
                f"Urgency: {report.urgency_level}\n"
                f"Location: {report.location or 'Unknown'}\n"
                f"Description: {decrypted_description}"
        )
        TWILIO_CLIENT.messages.create(
            body=msg, 
            from_=settings.TWILIO_FROM_NUMBER, 
            to=phone
            
        )
        report.assigned_to = authority_instance
        report.status = 'under_review'
        report.save()
        masked_phone = phone[:-4] + "****"
        logger.info(f"Successfully sent SMS to {authority_name} ({masked_phone}) for report {report.id}")
        AuditLog.objects.create(
            report=report, 
            action=action, 
            metadata={'authority': authority_name, 'phone': phone, 'case': decrypted_description}
        )
    except Exception as e:
        logger.error(f"sms failed because of error { str(e) }")
        AuditLog.objects.create(
            report=report, 
            action='sms_failed', 
            metadata={'authority': authority_name, 'error': str(e)}
            
        )
        

@shared_task()
def notify_authorities_task(report_id):
    report = Report.objects.get(pk=report_id)
    
    if report.location:
        coords = geocode_location(report.location)
        if not coords:
            logger.error(f"geocode_failed for report {report} of location {report.location}")
            AuditLog.objects.create(report=report, action='geocode_failed', metadata={'location': report.location})
            return
        latitude, longitude = coords
        station = get_nearest_police_station(latitude, longitude)
        if not station:
            logger.info(f"No nearby station for report #{report.id} at coordinates ({latitude}, {longitude})")           
            AuditLog.objects.create(report=report, action='no_nearby_station', metadata={'lat': latitude, 'lon': longitude})
            return
        if station.phone_number:
            # phone = station.phone_number onlyfor prod
            phone = settings.TWILIO_TEST_NUMBER
            send_twilio_sms(report, phone, station.name, 'notified_authority')
        else:
            # try phone number for state
            # contact_number = authority.state_phone_number #for production only
            contact_number = settings.TWILIO_TEST_NUMBER
            if contact_number:
                send_twilio_sms(report, contact_number, station.name, 'notified_authority')
