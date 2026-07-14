from celery import Celery
import os

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "news_api.settings"
)

app = Celery("news_api")

app.config_from_object(
    "django.conf:settings",
    namespace="CELERY"
)

app.autodiscover_tasks()