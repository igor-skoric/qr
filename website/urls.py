from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('all_codes', views.all_codes, name='all_codes'),
    path('code/<int:pk>', views.code, name='code'),
]
