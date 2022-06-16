import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings
# from mycelery import config

# 设置celery环境变量和django-celery的工作目录
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tutorial.settings")

# 实例化celery
cel = Celery("covid_ksh_demo")

# 加载celery配置
# cel.config_from_object("django.conf:settings")
cel.config_from_object("mycelery.config")

"""
# 如果项目当中有task.py, 那么celery使用app当中的task来生成任务
cel.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
"""
cel.autodiscover_tasks(["mycelery.covid_task", ])

cel.conf.timezone = 'Asia/Shanghai'
cel.conf.enable_utc = False


cel.conf.beat_schedule = {
    # 名字随意命名
    'do_once': {
        # 执行任务函数
        'task': 'mycelery.covid_task.tasks.start_get_data',
        # 每隔2秒执行一次
        # 'schedule': 1.0,
        'schedule': crontab(minute='02', hour='16', day_of_week='0-6', day_of_month='1-30', month_of_year='6'),
        # 'schedule': timedelta(seconds=6),
        # 传递参数
        # 'args': ('张三',)
    },
    # 'add-every-12-seconds': {
    #     'task': 'celery_tasks.task01.send_email',
    #     每年4月11号，8点42分执行
    #     'schedule': crontab(minute=42, hour=8, day_of_month=11, month_of_year=4),
    #     'args': ('张三',)
    # },
}

