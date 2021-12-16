from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Work, Category, Tag
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from django.db.models import Q

def new_comment(request, pk):
    if request.user.is_authenticated: # 로그인한 사용자
        work = get_object_or_404(Work, pk=pk) # 장고제공함수. 해당하는 pk값 없으면 페이지없다고 알려주는..
        if request.method == 'POST' :
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid() : # 올바르게 작성된 댓글 폼인지 확인
                comment = comment_form.save(commit=False)
                comment.work = work
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else :
            return redirect(work.get_absolute_url())
    else:
        raise PermissionDenied

# Create your views here.
# LoginRequiredMixin : 로그인한 방문자만 접근 가능하도록 하기
# UserPassesTestMixin : 특정 사용자만 접근 허용하기
class WorkCreate(LoginRequiredMixin,UserPassesTestMixin, CreateView): # 템플릿 : 모델명_form
    model = Work
    fields = ['title','description','price','head_image','category','commericial']

    def test_func(self):
        return self. request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form): # form 처리해주는 함수
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):  # 조건중에 하나만 통과해도 ok..
            form.instance.author = current_user
            response = super(WorkCreate,self).form_valid(form)
            tags_str = self.request.POST.get('tags_str') # tags 이름을 가지고있는..태그 안에 있는 데이터가져옴
            if tags_str :
                tags_str = tags_str.strip() # 불필요한 공백 제거
                tags_str = tags_str.replace(',',';') # ,로 구분된걸 ; 으로 변경
                tags_list = tags_str.split(';') # 태그 ; 기준으로 잘라서 list화
                for t in tags_list :
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    if is_tag_created : # 새로운 태그가 있으면 태그모델에 추가 및 슬러그만들어줌
                        tag.slug = slugify(t, allow_unicode=True) # 한글태그,슬러그 받을수잇도록..
                        tag.save() #변경된 태그내용 저장
                    self.object.tags.add(tag)
            return response
        else :
            return redirect('/artwork/')

class WorkUpdate(LoginRequiredMixin, UpdateView): # 템플릿 : 모델명_form
    model = Work
    fields = ['title','description','price','head_image','category','commericial']

    # 자동으로 생성되는 템플릿이름이 create 클래스랑 겹치므로 새롭게 만들어줌
    template_name = 'artwork/work_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author :
            return super(WorkUpdate, self). dispatch(request, *args, **kwargs)
        else :
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super(WorkUpdate, self).get_context_data()
        if self.object.tags.exists():
            tags_str_list = list()
            for t in self.object.tags.all():
                tags_str_list.append(t.name)
            context['tags_str_default'] = '; '.join(tags_str_list)
        return context

    def form_valid(self, form):  # form 처리해주는 함수
        response = super(WorkUpdate, self).form_valid(form)
        self.object.tags.clear() # 기존에 있던 태그 지움
        tags_str = self.request.POST.get('tags_str')  # tags 이름을 가지고있는..태그 안에 있는 데이터가져옴
        if tags_str:
            tags_str = tags_str.strip()  # 불필요한 공백 제거
            tags_str = tags_str.replace(',', ';')  # ,로 구분된걸 ; 으로 변경
            tags_list = tags_str.split(';')  # 태그 ; 기준으로 잘라서 list화
            for t in tags_list:
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t)
                if is_tag_created:  # 새로운 태그가 있으면 태그모델에 추가 및 슬러그만들어줌
                    tag.slug = slugify(t, allow_unicode=True)  # 한글태그,슬러그 받을수잇도록..
                    tag.save()  # 변경된 태그내용 저장
                self.object.tags.add(tag)
        return response

class WorkList(ListView) : # 작품 목록 페이지
    model = Work
    ordering = '-pk'
    paginate_by = 6
# work_list.html
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkList,self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_work_count'] = Work.objects.filter(category=None).count()
        return context

class WorkDetail(DetailView):  # 작품 상세 페이지
    model = Work
# work_detail.html
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkDetail,self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_work_count'] = Work.objects.filter(category=None).count()
        context['comment_form'] = CommentForm
        return context

class WorkSearch(WorkList) :
    paginate_by = None

    def get_queryset(self):
        q = self.kwargs['q']
        work_list = Work.objects.filter(
            Q(title__contains=q) | Q(tags__name__contains=q) # 두개의 쿼리 통과하면... 전달됨
        ).distinct()
        return work_list

    def get_context_data(self, **kwargs):
        context = super(WorkSearch,self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'{q} - {self.get_queryset().count()}개의 작품'

        return context

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