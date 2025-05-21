from django.db import models
from django.contrib.auth.models import User
from CollectionPoint.models import CV
from UserManagement.models import JobSeekerProfile

class EmailHistory(models.Model):
    """Historial de correos enviados"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cv = models.ForeignKey(CV, on_delete=models.SET_NULL, null=True, blank=True)
    recipient_email = models.EmailField()
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('success', 'Enviado exitosamente'),
        ('failed', 'Falló el envío'),
    ])
    error_message = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Email a {self.recipient_email} - {self.sent_at.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        verbose_name = "Historial de correo"
        verbose_name_plural = "Historial de correos"
        ordering = ['-sent_at']