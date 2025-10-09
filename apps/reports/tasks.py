from celery import shared_task
from django.conf import settings
import requests
from twilio.rest import Client
from .models import Report, AuditLog
from apps.authorities.models import Authority
from math import radians, sin, cos, sqrt, atan2



API_KEY = settings.LOCATIONIQ_API_KEY
TWILIO_CLIENT = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)


def geocode_location(location_name):
    url = f"https://us1.locationiq.com/v1/search.php"
    params = {
        "key": API_KEY,
        "q": location_name,
        "format": "json",
        "limit": 1,
        "countrycodes": "KE"  # restricting to Kenya for mvp
    }
    response = requests.get(url, params=params)
    data = response.json()

    if isinstance(data, list) and data:
        return float(data[0]["lat"]), float(data[0]["lon"])
    
    print("Error or no results:", data)  
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
    for station in Authority.objects.all():
        dist = haversine(lat, lon, station.latitude, station.longitude)
        if dist < min_dist:
            nearest = station
            min_dist = dist
    return nearest


@shared_task()
def notify_authorities_task(reportId):
    report = Report.objects.get(pk=reportId)
    
    contact = None
    authority = None
    if report.location:
        latitude, longitude = geocode_location(report.location)
        station = get_nearest_police_station(latitude, longitude)
        if station.phone_number:
            # phone = station.phone_number
            phone = settings.TWILIO_FROM_NUMBER

            msg = f"New report: urgency {report.urgency}. Location: {report.location or 'unknown'}"
            try:
                TWILIO_CLIENT.messages.create(
                    body=msg,
                    from_=settings.TWILIO_FROM_NUMBER,
                    to=phone
                )
                AuditLog.objects.create(report=report, action='notified_external_phone', metadata={'phone': phone})
            except Exception as e:
                AuditLog.objects.create(report=report, action='sms_failed', metadata={'error': str(e)})
        else:
            # try phone number for state
            authority = station

            if (authority):
                # contact_number = authority.state_phone_number #for production env
                contact_number = settings.TWILIO_TEST_NUMBER
                if contact_number:
                    try:
                        TWILIO_CLIENT.messages.create(body=f"New report: {report}", from_=settings.TWILIO_FROM_NUMBER, to=contact_number)
                        report.assigned_to = station
                        report.status = 'under_review'
                        report.save()
                        AuditLog.objects.create(report=report, action='notified_authority', performed_by=None, metadata={'authority': authority.name})
                    except Exception as e:
                        AuditLog.objects.create(report=report, action='sms_failed', metadata={'authority': authority.name, 'error': str(e)})
                        
