import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
app = Celery("bookmarks")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "Backup Database": {
        "task": "backup_db",
        "schedule": crontab(
            minute="0", hour="1", day_of_week="0"
        ),  # run every sundays at 1:00 AM
    },
}
