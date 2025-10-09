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
