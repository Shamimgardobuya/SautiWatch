from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Report, AuditLog
from .tasks import notify_authorities_task

@receiver(post_save,sender=Report)
def send_sms_signal(sender, instance, created, **kwargs):
    try:
        if created:
            reportId = instance.id
            notify_authorities_task.delay(reportId)
         
    except Exception as e:
            print(str(e))
            AuditLog.objects.create(report=instance, action='sms_failed', metadata={'error': str(e)})
        