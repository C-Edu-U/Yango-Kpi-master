from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_view, name='landing'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('agents/', views.agents_view, name='agents'),
    path('agents/edit/<str:operator_login>/', views.edit_agent_view, name='edit_agent'),
    path('agents/delete/<str:operator_login>/', views.delete_agent_view, name='delete_agent'),
    path('weekly-metrics/', views.weekly_metrics_view, name='weekly_metrics'),
    path('qa-evaluations/', views.qa_evaluations_view, name='qa_evaluations'),
    path('report/weekly/', views.weekly_metrics_report_view, name='weekly_metrics_report'),
    path('report/qa/', views.qa_report_view, name='qa_report'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('download/weekly_pdf/', views.download_weekly_metrics_pdf, name='download_weekly_pdf'),
    path('download/qa_pdf/', views.download_qa_pdf, name='download_qa_pdf'),
    path('download/dashboard_pdf/', views.download_dashboard_pdf, name='download_dashboard_pdf'),
    path('qa-evaluations/add-comments/<str:evaluation_key>/', views.add_comments_view, name='add_comments'),
]
