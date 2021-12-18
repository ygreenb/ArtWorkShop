from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [ #서버IP/
    path('',views.langing),#서버IP/ #대문페이지
    path('about_us/', views.about_us), #서버IP/about_us/ # 회사소개 페이지
    path('mypage/', views.my_page),  # 서버IP/mypage/ # 마이페이지
    path('mywork/', views.my_work),  # 서버IP/mywork/ # 나의작품리스트
]