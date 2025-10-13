from django.urls import path
from . import views
from .views import ReportListCreateView, ReportDetailView, RegionListView

urlpatterns = [
    path('api/regions/', RegionListView.as_view(), name='region-list'),
    path('api/reports/', ReportListCreateView.as_view(), name='report-list'),
    path('api/reports/<int:pk>/', ReportDetailView.as_view(), name='report-detail'),


    path('api/reports/<int:report_id>/assign/', views.assign_report, name='assign_report'),
    path('api/reports/<int:report_id>/resolve/', views.resolve_report, name='resolve_report'),
]