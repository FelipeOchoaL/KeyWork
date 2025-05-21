# KeyWorkProject/MailSending/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('export-cv/<int:cv_id>/', views.export_cv_json, name='export_cv_json'),
    path('send-cv/<int:cv_id>/', views.send_cv_email_view, name='send_cv_email'),
    path('email-history/', views.email_history, name='email_history'),
]