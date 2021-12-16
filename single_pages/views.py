from django.shortcuts import render
from artwork.models import Work, Creator, Comment

# Create your views here.

def langing(request):
    recent_works = Work.objects.order_by('-pk')[:3]  # 최신 포스트
    return render(request, 'single_pages/home.html',
                  {'recent_works': recent_works})


def about_us(request):
    return render(request, 'single_pages/about_us.html')


def my_page(request):
    creator_list = Creator.objects.all()
    comment_list = Comment.objects.all()
    return render(request, 'single_pages/my_page.html',
                  {
                      'creator_list': creator_list,
                      'comment_list': comment_list
                  })
