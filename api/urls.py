from django.urls import path, re_path, include
from api import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'userlist', views.UserList)

urlpatterns = [
    path('v1/auth/', views.AuthView.as_view()),
    # path('v1/userlist/', views.UserView.as_view()),
    re_path(r'^(?P<version>[v1|v2]+)/userlist/$', views.UserView.as_view()),
    re_path(r'^(?P<version>[v1|v2]+)/rolelist/$', views.RoleView.as_view()),
    re_path(r'^(?P<version>[v1|v2]+)/UserInfolist/$', views.UserInfoView.as_view()),
    re_path(r'^(?P<version>[v1|v2]+)/Grouplist/(?P<pk>\d+)$', views.GroupView.as_view(), name='group_view'),
    re_path(r'^(?P<version>[v1|v2]+)/UserGroup/$', views.UserGroupView.as_view()),
    re_path(r'^(?P<version>[v1|v2]+)/UserlistPager/$', views.PagerView.as_view()),

    re_path(r'^(?P<version>[v1|v2]+)/', include(router.urls)),
]











# re_path(r'^(?P<version>[v1|v2]+)/UserlistViewSet/$', views.UserList.as_view({'get': 'list', 'post': 'create'})),
# re_path(r'^(?P<version>[v1|v2]+)/UserlistViewSet/(?P<pk>\d+)/$',
#         views.UserList.as_view({'get': 'retrieve',
#                                 # 'post': 'create',
#                                 'put': 'update',
#                                 'delete': 'destroy',
#                                 'patch': 'partial_update'})),