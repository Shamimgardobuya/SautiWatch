from django.urls import path
from . import views

urlpatterns = [
    path('report/', views.report_create_view, name='report_create'),
    path('report/success/', views.report_success_view, name='report_success'),
    path('reports/', views.report_list_view, name='report_list'),
    path('reports/<int:pk>/update/', views.report_update_view, name='report_update'),
]