# KeyWorkProject/MailSending/utils.py
import json
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
import os
from django.core.mail import EmailMessage
from django.conf import settings
import io
def cv_to_json(cv, profile):
    """
    Convierte un CV y perfil de usuario a formato JSON.
    
    Args:
        cv: Objeto CV
        profile: Objeto JobSeekerProfile
        
    Returns:
        str: Representación JSON del CV
    """
    # Extraer habilidades y lenguajes como listas
    skills = [skill.strip() for skill in profile.skills.split(',')] if profile.skills else []
    languages = [lang.strip() for lang in profile.languages.split(',')] if profile.languages else []
    
    # Crear diccionario con los datos del CV
    cv_data = {
        'personal_info': {
            'full_name': profile.full_name or '',
            'professional_title': profile.professional_title or '',
            'phone_number': profile.phone_number or '',
            'email': profile.user.email,
            'location': profile.location or '',
        },
        'professional_info': {
            'years_experience': profile.years_experience or 0,
            'skills': skills,
            'languages': languages,
            'education': profile.education or '',
            'availability': profile.get_availability_display() if profile.availability else '',
            'desired_salary': str(profile.desired_salary) if profile.desired_salary else '',
            'remote_work': profile.remote_work,
        },
        'cv_info': {
            'upload_type': cv.get_upload_type_display(),
            'uploaded_at': cv.uploaded_at.strftime('%Y-%m-%d %H:%M:%S'),
            'extracted_text': cv.extracted_text or '',
        },
        'metadata': {
            'exported_at': '',  # Se llenará al momento de exportar
            'version': '1.0',
            'source': 'KeyWork Platform'
        }
    }
    
    return json.dumps(cv_data, indent=4, ensure_ascii=False)

def send_cv_email(user, cv_json, recipient_email, filename):
    """
    Envía el CV en formato JSON por correo electrónico - Incluye el JSON en el cuerpo del correo.
    """
    try:
        # Preparar el correo electrónico
        subject = f"CV de {user.get_full_name() or user.username} - Enviado desde KeyWork"
        
        body = f"""
        <html>
        <body>
            <h2>Hola, Magneto Empleos</h2>
            <p>{user.get_full_name() or user.username} ha enviado su Curriculum Vitae para su consideración.</p>
            <p>El CV ha sido adjuntado a este correo en formato JSON para facilitar su procesamiento.</p>
            <p>También se incluye a continuación en el cuerpo del correo:</p>
            <pre style="background-color: #f5f5f5; padding: 10px; border-radius: 5px; overflow: auto;">{cv_json}</pre>
            <p>Este es un correo automático enviado desde KeyWork.</p>
        </body>
        </html>
        """
        
        from django.core.mail import EmailMessage
        from django.conf import settings
        
        # Crear la instancia de EmailMessage
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient_email],
        )
        email.content_subtype = "html"
        
        # Adjuntar como archivo también (intento adicional)
        email.attach(filename, cv_json.encode('utf-8'), 'application/json')
        
        # Enviar el correo
        email.send(fail_silently=False)
        
        return True, None
    except Exception as e:
        # Registrar el error
        import traceback
        error_message = f"{str(e)}\n{traceback.format_exc()}"
        print(f"Error sending email: {error_message}")
        return False, error_message