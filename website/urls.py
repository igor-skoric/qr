from django.urls import path
from . import views
from .admin import admin_site

app_name = 'website'

urlpatterns = [
    path('myadmin/', admin_site.urls, name='myadmin'),
    path('', views.home, name='home'),
    path('all_codes/', views.all_codes, name='all_codes'),
    path('code/<int:pk>', views.code, name='code'),
    path('upload_image/', views.upload_image, name='upload_image'),
    path('image_upload/', views.image_upload, name='image_upload'),
]
