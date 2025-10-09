from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.report_create_view, name='report_create'),
    path('report/track/', views.report_track_view, name='report_track'),
    path('report/success/', views.report_success_view, name='report_success'),
    path('reports/', views.report_list_view, name='report_list'),
    path('reports/reports/<str:tracking_id>/', views.report_detail_view, name='report_detail'),
    path('dashboard/reports/search/', views.report_search_view, name='report_search'),
]