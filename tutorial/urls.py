"""tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView
from rest_framework.documentation import include_docs_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('app01/', include('app01.urls')),
    path('api/', include('api.urls')),
    path('app02/', include('app02.urls')),
    path('covid_ksh/', include('covid_ksh_demo.urls')),
    # path('order/', )
    path('doc/', include_docs_urls(title='test')),
    path('', RedirectView.as_view(url='covid_ksh/v1/COVID-19')),  # 中国累计新增/确诊折线图
    # path('api-auth/', include('rest_framework.urls')),
]
