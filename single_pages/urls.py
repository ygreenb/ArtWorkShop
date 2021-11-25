from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [ #서버IP/
    path('',views.langing),#서버IP/ #대문페이지
    path('about_us/', views.about_us) #서버IP/about_us/ #회사소개 페이지
]