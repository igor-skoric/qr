from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('all_codes', views.all_codes, name='all_codes'),
    path('code/<int:pk>', views.code, name='code'),
    path('upload_image', views.upload_image, name='upload_image'),
    path('image_upload', views.image_upload, name='image_upload'),
]
