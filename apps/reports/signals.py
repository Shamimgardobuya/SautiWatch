from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Report, AuditLog
from .tasks import notify_authorities_task
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Report)
def send_sms_signal(sender, instance, created, **kwargs):
    if not created:
        return 
    try:
        notify_authorities_task.delay(instance.id)
    except Exception as e:
        logger.error(f"Signal failed for report {instance.id}: {str(e)}")
        AuditLog.objects.create(
            report=instance,
            action='sms_failed',
            metadata={'error': str(e)}
        )
