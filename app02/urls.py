from django.urls import re_path, include
from app02 import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'course-list', views.App02CourseView)
router.register(r'degree-course', views.App02DegreeCourseView)
router.register(r'course-prices', views.App02PricePolicy)

urlpatterns = [
    re_path(r'^(?P<version>[v1|v2]+)/', include(router.urls)),
]
# urlpatterns = router.urls
