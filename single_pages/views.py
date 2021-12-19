from django.shortcuts import render
from artwork.models import Work, Creator, Comment, Category
from django.db.models import Q

# Create your views here.

def langing(request):
    recent_works = Work.objects.order_by('-pk')[:3]  # 최신 포스트
    return render(request, 'single_pages/home.html',
                  {'recent_works': recent_works})


def about_us(request):
    return render(request, 'single_pages/about_us.html',
                  {
                      'categories' : Category.objects.all()
                  })

def my_page(request):
    creator_list = Creator.objects.all()
    comment_list = Comment.objects.all().order_by('-pk')
    return render(request, 'single_pages/my_page.html',
                  {
                      'creator_list': creator_list,
                      'comment_list': comment_list,
                  })

def my_work(request):
    work_list = Work.objects.all().order_by('-pk')

    return render(request, 'single_pages/my_work.html',
                  {
                      'work_list' : work_list
                  })

def creator_page(request,slug):
    creator = Creator.objects.get(slug=slug)
    creator_list = Creator.objects.all()
    creator_work = creator.work_set.all().order_by('-pk')

    return render(request, 'single_pages/my_work.html',
                  {
                      'creator' : creator,
                      'creator_list' : creator_list,
                      'creator_work' : creator_work
                  })
