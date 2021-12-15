from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from .models import Work, Category, Tag
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.
# LoginRequiredMixin : 로그인한 방문자만 접근 가능하도록 하기
class WorkCreate(LoginRequiredMixin, CreateView):
    model = Work
    fields = ['title','description','price','head_image','author','category','tags','commericial']

    # def test_func(self):
    #     return self. request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form): # form 처리해주는 함수
        current_user = self.request.user
        if current_user.is_authenticated : # 조건중에 하나만 통과해도 ok..
            form.instance.author = current_user
            response = super(WorkCreate,self).form_valid(form)
            # tags_str = self.request.POST.get('tags_str') # tags 이름을 가지고있는..태그 안에 있는 데이터가져옴
            # if tags_str :
            #     tags_str = tags_str.strip() # 불필요한 공백 제거
            #     tags_str = tags_str.replace(',',';') # ,로 구분된걸 ; 으로 변경
            #     tags_list = tags_str.split(';') # 태그 ; 기준으로 잘라서 list화
            #     for t in tags_list :
            #         t = t.strip()
            #         tag, is_tag_created = Tag.objects.get_or_create(name=t)
            #         if is_tag_created : # 새로운 태그가 있으면 태그모델에 추가 및 슬러그만들어줌
            #             tag.slug = slugify(t, allow_unicode=True) # 한글태그,슬러그 받을수잇도록..
            #             tag.save() #변경된 태그내용 저장
            #         self.object.tags.add(tag)
            # return response
        else :
            return redirect('/artwork/')

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
    work_list = tag.work_set.all() #Work.objects.filter(tags=tag)

    return render(request, 'artwork/work_list.html',
                  {
                      'work_list' : work_list,
                      'categories' : Category.objects.all(),
                      'no_category_work_count' : Work.objects.filter(category=None).count(),
                      'tag' : tag
                  }
                  )