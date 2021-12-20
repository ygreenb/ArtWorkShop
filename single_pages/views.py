from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView
from artwork.models import Work, Creator, Comment, Category
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied

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

class CreatorCreate(LoginRequiredMixin,UserPassesTestMixin, CreateView): # 템플릿 : 모델명_form
    model = Creator
    fields = ['name','slug','profile_image','intro','email','address','contact']

    def test_func(self):
        return self. request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form): # form 처리해주는 함수
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):  # 조건중에 하나만 통과해도 ok..
            form.instance.author = current_user
            response = super(CreatorCreate,self).form_valid(form)

            return response
        else :
            return redirect('/')

class CreatorUpdate(LoginRequiredMixin, UpdateView): # 템플릿 : 모델명_form
    model = Creator
    fields = ['name','slug','profile_image','intro','email','address','contact']
    template_name = 'artwork/creator_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author :
            return super(CreatorUpdate, self). dispatch(request, *args, **kwargs)
        else :
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super(CreatorUpdate, self).get_context_data()
        return context

    def form_valid(self, form): # form 처리해주는 함수
        response = super(CreatorUpdate, self).form_valid(form)
        return response


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
