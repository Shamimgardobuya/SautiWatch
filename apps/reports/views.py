from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Report, Region
from .forms import ReportForm, ReportUpdateForm
import hashlib

# Create your views here.

def report_create_view(request):
    """Public form for submitting confidential reports"""
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.save()
            
            # Send notification to relevant authorities
            notify_authorities(report)
            
            messages.success(request, 'Your report has been submitted securely. Reference ID: #' + str(report.id))
            return redirect('report_success')
    else:
        form = ReportForm()
    
    return render(request, 'reports/create_report.html', {'form': form})


def report_success_view(request):
    """Success page after report submission"""
    return render(request, 'reports/report_success.html')


@login_required
@permission_required('reports.can_view_reports', raise_exception=True)
def report_list_view(request):
    """List all reports (for authorized users only)"""
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
@permission_required('reports.can_manage_reports', raise_exception=True)
def report_update_view(request, pk):
    """Update report status and assignment"""
    report = get_object_or_404(Report, pk=pk)
    
    if request.method == 'POST':
        form = ReportUpdateForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            messages.success(request, 'Report updated successfully.')
            return redirect('report_details', pk=pk)
    else:
        form = ReportUpdateForm(instance=report)
    
    return render(request, 'reports/report_update.html', {'form': form, 'report': report})

@login_required
@permission_required('reports.can_manage_reports', raise_exception=True)
def report_detail_view(request, pk):
    report = get_object_or_404(Report, pk=pk)
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
