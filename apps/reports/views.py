from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Report, Region
from .forms import ReportForm


# Create your views here.

def report_create_view(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.save()
            
            notify_authorities(report)
            
            messages.success(request, 'Your report has been submitted securely.')
            return render(request, 'reports/success.html', {'tracking_id': report.tracking_id})
        else:
            print(form.errors)
    else:
        form = ReportForm()
    
    return render(request, 'reports/create_report.html', {'form': form})


def report_success_view(request):
    """Success page after report submission"""
    return render(request, 'reports/report_success.html')

def report_track_view(request):
    tracking_id = request.GET.get('tracking_id', '')
    report = None

    if tracking_id:
        try:
            report = Report.objects.get(tracking_id=tracking_id)
        except Report.DoesNotExist:
            messages.error(request, 'Invalid tracking ID')

    return render(request, 'reports/track.html', {
        'report': report,
        'tracking_id': tracking_id
    })


@login_required
@permission_required('reports.can_view_reports', raise_exception=True)
def report_list_view(request):
    #List all reports (for authorized users only)
    reports = Report.objects.select_related('region', 'assigned_to').all()
    
    # Filter by status if provided
    status = request.GET.get('status')
    if status:
        reports = reports.filter(status=status)
    
    # Filter by urgency if provided
    urgency = request.GET.get('urgency')
    if urgency:
        reports = reports.filter(urgency_level=urgency)
    
    return render(request, 'reports/report_list.html', {'reports': reports})


@login_required
@permission_required('reports.view_report', raise_exception=True)
def report_search_view(request):
    search_query = request.GET.get('q', '').strip()
    reports = Report.objects.select_related('region').none()
    
    if search_query and len(search_query) >= 2:
        reports = Report.objects.select_related('region').filter(
            Q(tracking_id__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(region_icontains=search_query)
        )
        
        status = request.GET.get('status', '')
        if status:
            reports = reports.filter(status=status)
        
        urgency = request.GET.get('urgency', '')
        if urgency:
            reports = reports.filter(urgency_level=urgency)
        
        region_id = request.GET.get('region', '')
        if region_id:
            reports = reports.filter(region_id=region_id)
        
        # Sorting
        sort_by = request.GET.get('sort', '-created_at')
        valid_sorts = ['created_at', '-created_at', 'urgency_level', '-urgency_level', 
                       'status', 'incident_date', '-incident_date', 'tracking_id']
        if sort_by in valid_sorts:
            reports = reports.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(reports, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all regions for filter dropdown
    all_regions = Region.objects.all()
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'results_count': reports.count() if search_query else 0,
        'status_choices': Report.STATUS_CHOICES,
        'urgency_choices': Report.URGENCY_CHOICES,
        'all_regions': all_regions,
        'current_status': request.GET.get('status', ''),
        'current_urgency': request.GET.get('urgency', ''),
        'current_region': request.GET.get('region', ''),
        'current_sort': request.GET.get('sort', '-created_at'),
    }
    
    return render(request, 'reports/search.html', context)

@login_required
@permission_required('reports.can_manage_reports', raise_exception=True)
def report_detail_view(request, tracking_id):
    report = get_object_or_404(Report, tracking_id=tracking_id)
    context = {
        "report": report
    }
    return render(request, "reports/report_detail.html", context)

def notify_authorities(report):
    """Send email notification to relevant authorities"""
    try:
        subject = f'[URGENT] New Report #{report.id} - {report.get_urgency_level_display()} Priority'
        message = f"""
A new confidential report has been submitted.

Report ID: #{report.id}
Urgency: {report.get_urgency_level_display()}
Location: {report.location}
Region: {report.region.name if report.region else 'Not specified'}
Date of Incident: {report.incident_date.strftime('%Y-%m-%d %H:%M')}
Status: {report.get_status_display()}

Please log in to the system to view full details.

This is an automated message. Do not reply to this email.
        """
        
        # Send to region contact if available
        recipient_list = []
        if report.region and report.region.contact_email:
            recipient_list.append(report.region.contact_email)
        
        # Also send to admin email
        recipient_list.append(settings.ADMIN_EMAIL)
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
            fail_silently=False,
        )
    except Exception as e:
        print(f"Failed to send notification: {e}")
