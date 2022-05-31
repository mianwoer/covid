from django.contrib import admin
from django.urls import path, include
from app01 import views

urlpatterns = [
    path('uu/', views.show),
    path('cbv/', views.Show1.as_view()),
]
