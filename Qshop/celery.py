import os
from celery import Celery
from django.conf import settings

# 设celery的环境变量和django-celery的工作目录
os.environ.setdefault("DJANGO_SETTINGS_MODULE","Celery.settings")
# 实例化celery应用
app = Celery("art_project")
# 加载celery配置
app.config_from_object("django.conf:settings")
# 生成任务  INSTALLED_APPS:已安装的app
app.autodiscover_tasks(lambda :settings.INSTALLED_APPS)
