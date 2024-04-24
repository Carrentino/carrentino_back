from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from django.conf import settings

# Устанавливаем переменную окружения DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Используем настройки Django в качестве настроек Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение задач в файлах tasks.py внутри приложений Django
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
