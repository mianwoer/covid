from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin

from api.utils.auth import MyCursorPagination
from app02 import models
from app02.serializers import CourseSerializer, DegreeCourseSerializer, PricePolicySerializer


class App02CourseView(ModelViewSet):
    authentication_classes = []
    permission_classes = []
    pagination_class = MyCursorPagination
    serializer_class = CourseSerializer
    queryset = models.Course.objects.all()


class App02DegreeCourseView(ModelViewSet):
    authentication_classes = []
    permission_classes = []
    pagination_class = MyCursorPagination
    serializer_class = DegreeCourseSerializer
    queryset = models.DegreeCourse.objects.all()


class App02PricePolicy(CreateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    authentication_classes = []
    permission_classes = []
    pagination_class = MyCursorPagination
    serializer_class = PricePolicySerializer
    queryset = models.PricePolicy.objects.all()

    def create(self, request, *args, **kwargs):
        print(request.body)
        assert request.body
        ser = PricePolicySerializer(data=request.data)
        if ser.is_valid():
            try:
                course_obj = models.Course.objects.filter(title=request.data.get('course')).first()
                models.PricePolicy.objects.create(price=request.data.get('price'),
                                                  period=request.data.get('period'),
                                                  content_object=course_obj)
                return Response({
                    "ret": r''''{}'价格策略添加成功'''.format(request.data.get('course'))
                })
            except Exception as e:
                raise e
        else:
            print(ser.errors)
            return Response(ser.errors)

    def List(self, request, *args, **kwargs):
        # assert request.data
        ret = models.PricePolicy.objects.all()
        ser = PricePolicySerializer(instance=ret, many=True)
        return Response(ser.data)

