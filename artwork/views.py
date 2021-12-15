from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Work, Category, Tag

# Create your views here.

class WorkList(ListView) : # 작품 목록 페이지
    model = Work
    ordering = '-pk'
# work_list.html
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkList,self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_work_count'] = Work.objects.filter(category=None).count()
        return context

class WorkDetail(DetailView):  # 작품 상세 페이지
    model = Work
# work_detail.html

def category_page(request, slug): # 카테고리 페이지
    if slug == 'no_category' :
        category = '미분류'
        work_list = Work.objects.filter(category=None)
    else :
        category = Category.objects.get(slug=slug)
        work_list = Work.objects.filter(category=category)
    return render(request, 'artwork/work_list.html',
                  {
                      'work_list' : work_list,
                      'categories' : Category.objects.all(),
                      'no_category_work_count' : Work.objects.filter(category=None).count(),
                      'category' : category
                  }
                  )

def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    work_list = tag.work_set.all() #Post.objects.filter(tags=tag)

    return render(request, 'artwork/work_list.html',
                  {
                      'work_list' : work_list,
                      'categories' : Category.objects.all(),
                      'no_category_work_count' : Work.objects.filter(category=None).count(),
                      'tag' : tag
                  }
                  )