from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdown

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/artwork/tag/{self.slug}'

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # slug : Work의 pk 대신에 사용하는 필드로 text를 통해서 url 만들어주고싶을 때 사용함.
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/artwork/category/{self.slug}'

    class Meta: # 대응되는 문자열로 바꿀수있게 해주는 클래스
        verbose_name_plural = 'Categories'

class Creator(models.Model):
    name = models.CharField(max_length=50, unique=True)  # 작가명
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # 다대일관계
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    # 이미지 파일 저장할 수 있는 imageField
    profile_image = models.ImageField(upload_to='artwork/images/%Y/%M/%d/', blank=True)

    intro = models.CharField(max_length=100, unique=True)  # 작가 한줄소개
    email = models.CharField(max_length=100, unique=True) # 이메일
    address = models.CharField(max_length=100, unique=True, blank=True)  # 주소(선택)
    contact = models.CharField(max_length=50, unique=True)  # 연락처

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return f'/artwork/{self.slug}'

class Work(models.Model):
    title = models.CharField(max_length=100)
    description = MarkdownxField()
    #price = models.CharField(max_length=100)
    price = models.IntegerField()

    # 이미지 파일 저장할 수 있는 imageField
    head_image = models.ImageField(upload_to='artwork/images/%Y/%M/%d/', blank=True)

    author = models.ForeignKey(User,on_delete=models.CASCADE) # 다대일관계
    creator = models.ForeignKey(Creator,null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL) # 다대일 관계
    tags = models.ManyToManyField(Tag, blank=True) # 다대다관계
    commericial = models.CharField(max_length=100) # 상업/비상업

    def __str__(self):
        return f'[{self.pk}]{self.title} :: {self.author}'

    def get_absolute_url(self): # 상세 포스트주소
        return f'/artwork/{self.pk}'

    def get_description_markdown(self):
        return markdown(self.description) # 기존텍스트 html를 마크다운 형식으로 변경

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists() :
            return self.author.socialaccount_set.first().get_avatar_url()
        else :
            return 'https://doitdjango.com/avatar/id/403/06906de089c1792c/svg/{{self.author.email}}/'

class Comment(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE) # 한명의 유저가 여러개의 커멘트 입력
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author}::{self.content}'

    def get_absolute_url(self):
        return f'{self.work.get_absolute_url()}#comment-{self.pk}'

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists() :
            return self.author.socialaccount_set.first().get_avatar_url()
        else :
            return 'https://doitdjango.com/avatar/id/403/06906de089c1792c/svg/{{self.author.email}}/'
