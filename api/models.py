from django.db import models

# Create your models here.
from django.db import models


class UserGroup(models.Model):
    title = models.CharField(max_length=32)


class Role(models.Model):
    role = models.CharField(max_length=32)


class UserInfo(models.Model):
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=64)
    user_type_choices = ((1, '普通用户'),
                         (2, 'vip'),
                         (3, 'svip'))
    user_type = models.IntegerField(choices=user_type_choices)

    group = models.ForeignKey("UserGroup", on_delete=models.CASCADE)
    roles = models.ManyToManyField("Role")


class UserToken(models.Model):
    user = models.OneToOneField(to='UserInfo', on_delete=models.CASCADE)
    token = models.CharField(max_length=64)
    # expire_time = models.CharField(max_length=16)
