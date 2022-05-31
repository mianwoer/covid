import datetime
import time

from rest_framework import serializers
from covid_ksh_demo import models
from rest_framework.serializers import ModelSerializer

from covid_ksh_demo.models import Ssrd


class CnCovidHistorySerializer(ModelSerializer):
    class Meta:
        model = models.Gnlssj
        fields = '__all__'

    def validate(self, attrs):
        return attrs


class YqTodaySerializer(ModelSerializer):
    class Meta:
        model = models.Bentuxianyou31
        fields = '__all__'

    def validate(self, attrs):
        # attrs 是数据字典，包含request中post的数据
        return attrs


class YqEverydaySerializer(ModelSerializer):
    class Meta:
        model = models.Mrsj
        fields = '__all__'

    def validate(self, attrs):
        # attrs 是数据字典，包含request中post的数据
        return attrs


def time_diff(timestamp):
    onlineTime = datetime.datetime.fromtimestamp(timestamp)
    localTime = datetime.datetime.now()
    result = localTime - onlineTime
    hours = int(result.seconds / 3600)
    minutes = int(result.seconds % 3600 / 60)
    seconds = result.seconds % 3600 % 60
    if result.days > 0:
        x = f'{result.days}天前'
    elif hours > 0:
        x = f'{hours}小时前'
    elif minutes > 0:
        x = f'{minutes}分钟前'
    else:
        x = f'{seconds}秒前'
    return x

# 热门资讯
class ReDianSerializer(serializers.ModelSerializer):
    time_ago = serializers.SerializerMethodField()


    class Meta:
        model = Ssrd
        fields = "__all__"

    def get_time_ago(self, obj):
        time_ago = time_diff(int(time.mktime(time.strptime(obj.eventtime, '%Y-%m-%d %H:%M:%S'))))   #字符转换成时间戳
        return time_ago