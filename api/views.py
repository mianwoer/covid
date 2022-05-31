# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from django.shortcuts import HttpResponse
import json
from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet

from api import models
from api.serializers import UserGroupSerializer, GroupSerializer, UserInfoSerializer, RoleSerializer
from utils.crud import Exsql
from django.db import transaction
from api.utils.auth import Authentication, SvipPermission, Mythrottle
from rest_framework.versioning import URLPathVersioning
from rest_framework.parsers import JSONParser, FormParser


# class AuthView(View):
#     pass
def md5(username):
    import hashlib
    import time
    ctime = str(time.time())
    m = hashlib.md5(bytes(username, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()


class AuthView(APIView):
    """用于用户登录认证"""
    authentication_classes = []
    permission_classes = []
    throttle_classes = []

    def get(self, request, *args, **kwargs):
        return HttpResponse('该用户不存在！，请重新输入')

    def post(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': None}
        try:
            user = request._request.POST.get('username')
            pwd = request._request.POST.get('password')
            print(user, pwd)
            obj = models.UserInfo.objects.filter(username=user, password=pwd)
            # print(type(obj.username))
            if not obj:
                ret['code'] = 1001
                ret['msg'] = '用户名或者密码错误'
            else:
                # 为用户创建token
                token = md5(user)
                # 存在就更新，不存在就创建token
                # models.UserToken.objects.update_or_create(user=obj, defaults={'token': token})
                c = Exsql()
                userid = c.get_one('''select id from api_userinfo where password = %s AND  username = %s''', pwd, user)
                count = c.get_one('''select count(1) from api_usertoken where user_id = %s''', userid[0])
                if count[0] == 0:
                    with transaction.atomic():
                        c.insert('''insert into api_usertoken(token,user_id) values (%s,%s)''', token, userid[0])
                else:
                    with transaction.atomic():
                        c.update('''update api_usertoken set token=%s where user_id=%s''', token, userid[0])
                ret['msg'] = '登录成功'
                ret['token'] = token
        except Exception as e:
            print(e)
        return JsonResponse(ret)


class UserView(APIView):
    user_type_map = {1: '普通用户',
                     2: 'vip用户',
                     3: 'svip用户'}
    authentication_classes = [Authentication, ]
    permission_classes = [SvipPermission, ]
    throttle_classes = [Mythrottle, ]
    # versioning_class = QueryParameterVersioning
    versioning_class = URLPathVersioning  # 已在配置文件中设置，全局使用
    parser_classes = [JSONParser, FormParser]  # 已在配置文件中设置，全局使用

    def get(self, request, *args, **kwargs):
        self.dispatch
        try:
            with transaction.atomic():
                c = Exsql()
                sql = '''select username, user_type from api_userinfo order by username'''
                res = c.get_all_dict(sql)
            if len(res) == 0:
                ret = {'code': 1001,
                       'version': request.version,
                       'msg': '未查询到用户信息，请创建用户'}
            else:
                for i in res:
                    i['user_type'] = UserView.user_type_map[i['user_type']]
                ret = {'code': 1000,
                       'version': request.version,
                       # 'scheme': request.scheme,
                       'data': res}
        except Exception as e:
            print(e)
        return Response(ret)

    def post(self, request, *args, **kwargs):
        """仅验证request中的数据"""
        print(request._request.POST)
        print(request._request.body)
        print("request.data数据为：", request.data)
        print(request.body)
        change = json.dumps(request.data)
        print("change: ", type(change), change)
        return HttpResponse("用户列表")
        # return JsonResponse(change)


class RoleView(APIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = []

    def get(self, request, *args, **kwargs):
        # roles = models.Role.objects.all().values('id','role')
        roles = models.Role.objects.all()
        ser = RoleSerializer(instance=roles, many=True)
        ret = json.dumps(ser.data, ensure_ascii=False)
        # print(ret)
        return HttpResponse(ret)


class UserInfoView(APIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = []
    """ 使用序列化，多表连查 """

    def get(self, request, *args, **kwargs):
        users = models.UserInfo.objects.all()
        ser = UserInfoSerializer(instance=users, many=True, context={'request': request})
        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)

    """ 使用sql查询
    def get(self, request, *args, **kwargs):
        try:
            c = Exsql()
            res = c.get_all_dict('''SELECT 
                    t.id,
                    t.username,
                    t.password,
                -- 	t.group_id, 
                    y.title as 'group',
                    case t.user_type when 3 then "svip" when 1 then "普通用户" when 2 then "vip" end "用户类型"
                FROM `api_userinfo` t
                    inner join api_usergroup y
                on t.group_id = y.id
                # where t.id >3 and kjk is  go
                ''', )
            # print(res)
            # print(args, kwargs)
            ret = {'code': 200,
                   'msg': "查询成功",
                   'data': res}
            # if 'error' not in res:
            #     if len(res) != 0:
            #         ret = {'code': 200,
            #                'msg': '查询成功',
            #                'data': res
            #                }
            #     else:
            #         ret = {'code': 200,
            #                'msg': '未查询到数据',
            #                'data': res}
            # else:
            #     ret = {'code': 500,
            #            'msg': res['error']}
        except Exception as e:
            print(e)
            ret = {'code': 500,
                   'msg': '后台查询失败'}
        return JsonResponse(ret, json_dumps_params={'ensure_ascii': False})
        # return HttpResponse(ret)
    """


class GroupView(APIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = []

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        group_obj = models.UserGroup.objects.filter(pk=pk).first()
        ser = GroupSerializer(instance=group_obj, many=False)
        ret = json.dumps(ser.data, ensure_ascii=False)
        return Response(ret)


class UserGroupView(APIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = []

    ################ 数据校验 #########
    def post(self, request, *args, **kwargs):
        ser = UserGroupSerializer(data=request.data)
        if ser.is_valid():
            # print(ser.validated_data)
            return Response("数据验证通过")
        else:
            print(ser.errors)
            return Response(ser.errors)


class XXXValidator():
    '''自定义验证规则，一般不写，框架中通过钩子函数实现了功能'''

    def __init__(self, base):
        self.base = base

    def __call__(self, value):
        if not value.startswith(self.base):
            msg = "必须以 \'{}\'  开头".format(self.base)
            raise serializers.ValidationError(msg)


"""分页视图"""

from api.utils.auth import MyCursorPagination


class PagerView(APIView):

    def get(self, request, *args, **kwargs):
        users = models.UserInfo.objects.all()  # 1、获取queryset数据
        page_obj = MyCursorPagination()  # 2、创建分页器对象
        users_paged = page_obj.paginate_queryset(queryset=users, request=request)  # 3、将queryset传入分页器处理
        ser = UserInfoSerializer(instance=users_paged, many=True, context={'request': request})  # 4、将分页处理后的数据实例化
        print(type(ser.data), ser.data)
        # return Response(ser.data)
        return page_obj.get_paginated_response(ser.data)


class UserList(ModelViewSet):
    queryset = models.UserInfo.objects.all()
    serializer_class = UserInfoSerializer
    pagination_class = MyCursorPagination

    # def create(self, request, *args, **kwargs):


