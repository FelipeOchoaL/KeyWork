# KeyWorkProject/MailSending/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
import json
import os

from CollectionPoint.models import CV
from UserManagement.models import JobSeekerProfile
from .models import EmailHistory
from .utils import cv_to_json, send_cv_email

@login_required
def export_cv_json(request, cv_id):
    """Vista para exportar el CV a formato JSON"""
    cv = get_object_or_404(CV, pk=cv_id)
    
    # Verificar si el usuario tiene permiso para ver este CV
    try:
        jobseeker_profile = JobSeekerProfile.objects.get(user=request.user)
        if jobseeker_profile.cv != cv:
            messages.error(request, 'No tienes permiso para exportar este CV.')
            return redirect('cv_detail', pk=cv_id)
    except JobSeekerProfile.DoesNotExist:
        messages.error(request, 'No se pudo verificar tu perfil.')
        return redirect('home')
    
    # Generar el JSON
    try:
        cv_json = cv_to_json(cv, jobseeker_profile)
        
        # Añadir la fecha de exportación
        cv_data = json.loads(cv_json)
        cv_data['metadata']['exported_at'] = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        cv_json = json.dumps(cv_data, indent=4, ensure_ascii=False)
        
        # Preparar la descarga
        response = HttpResponse(cv_json, content_type='application/json')
        filename = f"cv_{request.user.username}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.json"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response
    except Exception as e:
        messages.error(request, f'Error al exportar el CV: {str(e)}')
        return redirect('cv_detail', pk=cv_id)

@login_required
def send_cv_email_view(request, cv_id):
    """Vista para enviar el CV por correo electrónico"""
    cv = get_object_or_404(CV, pk=cv_id)
    
    # Verificar si el usuario tiene permiso para ver este CV
    try:
        jobseeker_profile = JobSeekerProfile.objects.get(user=request.user)
        if jobseeker_profile.cv != cv:
            messages.error(request, 'No tienes permiso para enviar este CV.')
            return redirect('cv_detail', pk=cv_id)
    except JobSeekerProfile.DoesNotExist:
        messages.error(request, 'No se pudo verificar tu perfil.')
        return redirect('home')
    
    # Configurar el correo predeterminado de Magneto Empleos
    magneto_email = os.environ.get('MAGNETO_EMAIL', 'info@magnetoempleos.com')
    
    if request.method == 'POST':
        email = request.POST.get('email', magneto_email)
        
        # Generar el JSON
        try:
            cv_json = cv_to_json(cv, jobseeker_profile)
            
            # Verificación de depuración - imprime el tamaño del JSON
            print(f"Generated JSON size: {len(cv_json)} characters")
            
            # Generar nombre del archivo
            filename = f"cv_{request.user.username.replace(' ', '_')}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            # Verificación adicional
            print(f"Sending email to: {email}")
            print(f"Filename: {filename}")
            
            # Enviar el correo
            success, error_message = send_cv_email(request.user, cv_json, email, filename)
            
            # Registrar el envío
            EmailHistory.objects.create(
                user=request.user,
                cv=cv,
                recipient_email=email,
                status='success' if success else 'failed',
                error_message=error_message
            )
            
            if success:
                messages.success(request, f'CV enviado exitosamente a {email}')
            else:
                messages.error(request, f'Error al enviar el CV: {error_message}')
            
            return redirect('cv_detail', pk=cv_id)
        except Exception as e:
            messages.error(request, f'Error al enviar el CV: {str(e)}')
            return redirect('cv_detail', pk=cv_id)
    
    # Si es GET, mostrar la página para confirmar el envío
    return render(request, 'MailSending/send_email.html', {
        'cv': cv,
        'profile': jobseeker_profile,
        'default_email': magneto_email
    })

@login_required
def email_history(request):
    """Vista para ver el historial de correos enviados"""
    # Verificar si el usuario tiene perfil de JobSeeker
    try:
        jobseeker_profile = JobSeekerProfile.objects.get(user=request.user)
    except JobSeekerProfile.DoesNotExist:
        messages.error(request, 'Esta sección es solo para buscadores de empleo.')
        return redirect('home')
    
    # Obtener el historial de correos del usuario
    emails = EmailHistory.objects.filter(user=request.user).order_by('-sent_at')
    
    return render(request, 'MailSending/email_history.html', {
        'emails': emails
    })