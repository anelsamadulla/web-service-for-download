# data_sender/urls.py
from django.urls import path
from .views import data_sender, download_file, test

#URLConf module

urlpatterns = [
    path('user_data_info/', data_sender, name='data_sender'),
    path('download/<str:jwt_token>/', download_file, name='download_file'), 
    path('test/', test, name='test'),
]
