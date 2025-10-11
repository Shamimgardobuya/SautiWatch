from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from rest_framework.permissions import AllowAny
from .models import Report, Region
from .serializers import ReportSerializer, RegionSerializer

# Custom Permission Class

class CanViewReportsPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.has_perm('reports.can_view_reports')


# Region List API
class RegionListView(generics.ListAPIView):

    queryset = Region.objects.all().order_by('name')
    serializer_class = RegionSerializer
    permission_classes = []


#  Report List & Create API
class ReportListCreateView(generics.ListCreateAPIView):

    queryset = Report.objects.all().select_related('region', 'assigned_to').order_by('-created_at')
    serializer_class = ReportSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'urgency_level', 'region'] 
    search_fields = ['tracking_id', 'incident_description']
    ordering_fields = ['created_at', 'urgency_level']

    def get_permissions(self):
            if self.request.method == "POST": #allow only anonymous users to post without permission
                return [AllowAny()]
            return [permissions.IsAuthenticated(), CanViewReportsPermission()]  #protect for get request



#  Single Report Detail API

class ReportDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a single report (decrypted fields returned in serializer)
    PUT/PATCH: Update an existing report
    DELETE: Delete a report (if needed)
    """
    queryset = Report.objects.all().select_related('region', 'assigned_to')
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated, CanViewReportsPermission]


# --------------------------
# 👮 Reports Assigned to Current User (Authority)
# --------------------------
class MyAssignedReportsView(generics.ListAPIView):
    """
    GET: List reports assigned to the currently authenticated user.
    """
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated, CanViewReportsPermission]

    def get_queryset(self):
        return Report.objects.filter(assigned_to=self.request.user).select_related('region', 'assigned_to').order_by('-created_at')


# --------------------------
# 📊 Dashboard Summary API (Optional)
# --------------------------
from rest_framework.views import APIView

class ReportStatsView(APIView):
    """
    GET: Summary statistics for dashboard (e.g., counts by status)
    """
    permission_classes = [permissions.IsAuthenticated, CanViewReportsPermission]

    def get(self, request, *args, **kwargs):
        total_reports = Report.objects.count()
        pending = Report.objects.filter(status='pending').count()
        under_review = Report.objects.filter(status='under_review').count()
        resolved = Report.objects.filter(status='resolved').count()

        return Response({
            "total_reports": total_reports,
            "pending": pending,
            "under_review": under_review,
            "resolved": resolved,
        }, status=status.HTTP_200_OK)

@login_required
@permission_required('reports.can_view_reports', raise_exception=True)
def assign_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    report.mark_under_review(request.user)
    return JsonResponse({'message': f'Report {report.tracking_id} assigned and marked Under Review.'})


# 🔸 Mark report as resolved
@login_required
@permission_required('reports.can_view_reports', raise_exception=True)
def resolve_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    report.mark_resolved()
    return JsonResponse({'message': f'Report {report.tracking_id} marked as Resolved.'})
