import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sauti_watch.settings")

app = Celery("sauti_watch")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()