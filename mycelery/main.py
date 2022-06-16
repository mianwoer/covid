import os
from celery import Celery
from django.conf import settings

# 设置celery环境变量和django-celery的工作目录
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tutorial.settings")

# 实例化celery
cel = Celery("tutorial")

# 加载celery配置
# cel.config_from_object("django.conf:settings")
cel.config_from_object("config")

# 如果项目当中有task.py, 那么celery使用app当中的task来生成任务
cel.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
