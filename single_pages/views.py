from django.shortcuts import render
from artwork.models import Work, Creator, Comment, Category

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
    comment_list = Comment.objects.all()
    return render(request, 'single_pages/my_page.html',
                  {
                      'creator_list': creator_list,
                      'comment_list': comment_list,
                  })

def my_work(request):
    my_works = Work.objects.order_by('-pk')
    return render(request, 'single_pages/my_work.html',
                  {
                      'my_works' : my_works
                  })

def category_page(request, slug): # 카테고리 페이지
    if slug == 'no_category' :
        category = '미분류'
        work_list = Work.objects.filter(category=None)
    else :
        category = Category.objects.get(slug=slug)
        work_list = Work.objects.filter(category=category)
    return render(request, 'artwork/about_us.html',
                  {
                      'work_list' : work_list,
                      'categories' : Category.objects.all(),
                      'no_category_work_count' : Work.objects.filter(category=None).count(),
                      'category' : category
                  }
                  )
