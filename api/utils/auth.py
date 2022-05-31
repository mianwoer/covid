import time

from rest_framework import exceptions
from api import models
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import BasePermission
from rest_framework.throttling import BaseThrottle, SimpleRateThrottle
from utils.crud import Exsql


class Authentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.GET.get('token')  # 相当于 request._request.GET.get('token')
        token_obj = models.UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed('用户认证失败@@')
        return (token_obj.user, token_obj)

    def authenticate_header(self, request):
        pass


class SvipPermission(BasePermission):
    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        必须是SVIP才能访问
        """
        try:
            sql = '''select user_type from api_userinfo where id = 
            (select user_id from api_usertoken where token = %s)'''
            exsql = Exsql()
            # token = request._request.GET.get('token')
            token = request.GET.get('token')
            # print('token值为：', token)
            res = exsql.get_one_dict(sql, token)[0].get('user_type')
            # print('res值为：', res)
            if res != 3:
                raise exceptions.PermissionDenied('您尚未与有权限查看信息！！')
                return False
            return True
        except Exception:
            raise exceptions.PermissionDenied('不登录还想看？')

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        使用 ModelViewSet时需要用到该方法
        """
        return True


rec = {}


class Mythrottle(BaseThrottle):
    '''控制访问频率, 用一个用户60s内访问某个视图不应该超过5次'''

    def __init__(self):
        history = None

    def allow_request(self, request, view):
        # remote_addr = request._request.META.get('REMOTE_ADDR')  # 获取用户ip
        remote_addr = self.get_ident(request)
        if remote_addr not in rec:
            rec[remote_addr] = [time.time(), ]
            return True
        self.history = rec[remote_addr]
        while self.history and time.time() - self.history[0] > 10:
            del self.history[0]
        if len(self.history) < 5:
            self.history.append(time.time())
            return True

    def wait(self):
        '''还需要等待多久，单位秒'''
        return 10 - (time.time() - self.history[0])


class VisitThrottle(SimpleRateThrottle):
    '''继承内置SimpleRateThrottle，根据客户端ip进行访问频率控制, 同一个ip60s内访问某个视图不应该超过5次'''
    scope = "Liuzhu"  # 将scope添加到settings中并在此处引用

    def get_cache_key(self, request, view):
        return self.get_ident(request)


class UserThrottle(SimpleRateThrottle):
    '''继承内置SimpleRateThrottle，根据用户名进行访问频率控制, 同一个用户60s内访问某个视图不应该超过10次'''
    scope = "LiuzhuUser"  # 将scope添加到settings中并在此处引用

    def get_cache_key(self, request, view):
        return request.user.username


class MyVersioning():
    '''自定义的版本类，一般在视图内直接使用from rest_framework.versioning import QueryParameterVersioning'''

    def determine_version(self, request, *args, **kwargs):
        version = request.query_params.get('version')  # 等于request._request.GET.get('version')
        # version = 'liuzhu'#
        return version


from rest_framework.pagination import PageNumberPagination, CursorPagination


class MyPagination(PageNumberPagination):
    page_size = 1  # 默认每页展示1条
    page_query_param = 'page'  # 前端需要查询第几页
    page_size_query_param = 'page_size'  # 前端自定义每页展示几条数据
    max_page_size = 10  # 可设置的每页最大展示数量


class MyCursorPagination(CursorPagination):
    cursor_query_param = 'cursor'
    page_size = 2
    ordering = 'id'
