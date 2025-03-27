from django.urls import path
from . import views

urlpatterns = [
    path('agents/', views.agents_view, name='agents'),
    path('weekly-metrics/', views.weekly_metrics_view, name='weekly_metrics'),
    path('qa-evaluations/', views.qa_evaluations_view, name='qa_evaluations'),
    path('report/weekly/', views.weekly_metrics_report_view, name='weekly_metrics_report'),
    path('report/qa/', views.qa_report_view, name='qa_report'),
]