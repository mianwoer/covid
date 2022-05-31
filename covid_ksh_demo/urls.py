from django.urls import path, re_path, include
from covid_ksh_demo import views
from rest_framework import routers
from django.views.generic import RedirectView

router = routers.DefaultRouter()
router.register(r'HistoryData', views.HistoryData)
router.register(r'YQToday', views.YqToday)
router.register(r'YqEveryday', views.YqEveryday)

urlpatterns = [
    #接口化更新数据
    re_path(r'^(?P<version>[v1|v2]+)/', include(router.urls)),
    re_path(r'^(?P<version>[v1|v2]+)/HistoryDataUpdate', views.HistoryDataUpdate.as_view()),
    re_path(r'^(?P<version>[v1|v2]+)/YqTodayUpdate', views.YqTodayUpdate.as_view()),
    re_path(r'^(?P<version>[v1|v2]+)/YqEverydayUpdate', views.YqEverydayUpdate.as_view()),
    re_path(r'^(?P<version>[v1|v2]+)/SsrdUpdate', views.SsrdUpdate.as_view()),
    re_path(r'^(?P<version>[v1|v2]+)/XyyqUpdate', views.XyyqUpdate.as_view()),
    re_path(r'^(?P<version>[v1|v2]+)/FxdqUpdate', views.FxdqUpdate.as_view()),
    re_path(r'^(?P<version>[v1|v2]+)/PastTwoMonthUpdate', views.PastTwoMonthUpdate.as_view()),
    #结合js代码展示图表
    re_path(r'^(?P<version>[v1|v2]+)/xyqz', views.qgyq.as_view(), name='xyqz'),  # 中国累计新增/确诊折线图
    re_path(r'^(?P<version>[v1|v2]+)/COVID-19/', views.IndexView.as_view(), name='COVID-19'),  # 中国累计新增/确诊折线图
        # re_path(r'^(?P<version>[v1|v2]+)/xyqz/', views.qgyq.as_view(), name='xyqz'), # 中国累计新增/确诊折线图
    re_path(r'^(?P<version>[v1|v2]+)/zgdt/', views.Zgdt.as_view(), name='Zgdt'), # 中国地图
    re_path(r'^(?P<version>[v1|v2]+)/yqbt/', views.Yqbt.as_view(), name='yqbt'), # 饼图
    re_path(r'^(?P<version>[v1|v2]+)/bg/', views.Bg.as_view(), name='bg'), # 近期31省区市本土现有病例
    re_path(r'^(?P<version>[v1|v2]+)/gfx/', views.gfx1.as_view(), name='gfx'), # 高风险
    re_path(r'^(?P<version>[v1|v2]+)/zfx/', views.zfx1.as_view(), name='zfx'), # 中风险
    re_path(r'^(?P<version>[v1|v2]+)/fxdq/', views.fxdq1.as_view(), name='fxdq'), # 中风险
    re_path(r'^(?P<version>[v1|v2]+)/chinayq/', views.chinayq1.as_view(), name='chinayq'), # 更新时间
    re_path(r'^(?P<version>[v1|v2]+)/ssrd/', views.ssrd1.as_view(), name='ssrd'), # 实时热点

]
# urlpatterns = router.urls
