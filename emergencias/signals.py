# BACKEND_DJANGO/emergencias/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Emergencia
from django.contrib.auth import get_user_model
from twilio.rest import Client
from django.utils import timezone  

User = get_user_model()

def send_emergency_notification(admin_telefono, mensaje_sms, mensaje_whatsapp):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    # Enviar SMS
    try:
        sms = client.messages.create(
            body=mensaje_sms,
            to=admin_telefono,
            from_=settings.TWILIO_PHONE_NUMBER
        )
        print(f"SMS de emergencia enviado a {admin_telefono}. SID: {sms.sid}")
    except Exception as e:
        print(f"Error al enviar SMS a {admin_telefono}: {e}")

    # Enviar WhatsApp
    if settings.TWILIO_WHATSAPP_NUMBER:
        try:
            whatsapp = client.messages.create(
                from_=settings.TWILIO_WHATSAPP_NUMBER,
                body=mensaje_whatsapp,
                to=f'whatsapp:{admin_telefono}'
            )
            print(f"WhatsApp de emergencia enviado a {admin_telefono}. SID: {whatsapp.sid}")
        except Exception as e:
            print(f"Error al enviar WhatsApp a {admin_telefono}: {e}")

@receiver(post_save, sender=Emergencia)
def send_emergency_notifications_to_admins(sender, instance, created, **kwargs):
    if created and instance.usuario:  # Asegura de que haya un usuario asociado
        administradores = User.objects.filter(tipo_usuario='admin')  

        mensaje_sms = f"¡EMERGENCIA! Tipo: {instance.tipo}, Piso: {instance.piso if instance.piso else 'N/A'}, Estudiante: {instance.usuario.nombre}"

        # Asegúra de que instance.fecha esté en la zona horaria de Colombia
        colombia_tz = timezone.get_default_timezone()  # Obtiene la zona horaria configurada en Django
        fecha_colombia = timezone.localtime(instance.fecha, colombia_tz)

        mensaje_whatsapp = f"""
        ¡EMERGENCIA REPORTADA!
        Tipo: {instance.tipo}
        Piso: {instance.piso if instance.piso else 'N/A'}
        Reportada por: {instance.usuario.nombre}
        Fecha: {fecha_colombia.strftime('%d/%m/%Y %H:%M')}
        """

        for admin in administradores:
            if admin.telefono:
                send_emergency_notification(admin.telefono, mensaje_sms, mensaje_whatsapp)