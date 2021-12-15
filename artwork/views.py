from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Work

# Create your views here.

class WorkList(ListView) : # 작품 목록 페이지
    model = Work
    ordering = '-pk'
# work_list.html

class WorkDetail(DetailView):  # 작품 상세 페이지
    model = Work
# work_detail.html