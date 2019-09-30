"""web1127 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from car import views as car_views

urlpatterns = [
    path('', car_views.index),
    path('upload_img/', car_views.upload_img, name='upload_img'),
    path('info/', car_views.info, name='info'),
    path('car_img/<str:img_name>/', car_views.car_img, name='car_img'),
    path('admin/', admin.site.urls),
]
