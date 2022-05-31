from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey


# Create your models here.


class Course(models.Model):
    """普通课程"""
    title = models.CharField(max_length=32)
    # 仅用于反向查找
    price_policy_list = GenericRelation("PricePolicy")


class DegreeCourse(models.Model):
    """学位课程"""
    title = models.CharField(max_length=32)
    # 仅用于反向查找
    price_policy_list = GenericRelation("PricePolicy")


class PricePolicy(models.Model):
    """价格策略"""
    price = models.IntegerField()
    period = models.IntegerField()
    content_type = models.ForeignKey(ContentType, verbose_name="关联普通课程或学位课程", on_delete=models.CASCADE)
    course_id = models.IntegerField(verbose_name="关联普通课程或学位课程")
    # 快速实现contenttype操作
    content_object = GenericForeignKey("content_type", "course_id")
    """
        PricePolicy对象创建方式：
        cobj = DegreeCourse.objects.filter(title='rest_framework解析').first()
        PricePolicy.objects.create(price=9,period=1,content_object=cobj)
    """
