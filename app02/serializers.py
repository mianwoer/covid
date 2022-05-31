from rest_framework import serializers

from app02 import models
from rest_framework.serializers import ModelSerializer


class CourseSerializer(ModelSerializer):
    class Meta:
        model = models.Course
        fields = '__all__'

    def validate(self, attr):
        # print(self.data)
        return attr


class DegreeCourseSerializer(ModelSerializer):
    class Meta:
        model = models.DegreeCourse
        fields = '__all__'


class PricePolicySerializer(ModelSerializer):
    # course = serializers.CharField()
    # gg = serializers.CharField()
    class Meta:
        model = models.PricePolicy
        fields = '__all__'
        depth = 2

    def validate(self, attrs):
        #attrs 是数据字典，包含request中post的数据
        course_name = attrs.get('course', 0)
        print(course_name, attrs)
        if course_name == 0:
            msg = "course 不能为空"
            raise serializers.ValidationError(msg)
        return attrs
