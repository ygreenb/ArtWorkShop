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

class Work(models.Model):
    title = models.CharField(max_length=100)
    description = MarkdownxField()
    price = models.CharField(max_length=100)

    # 이미지 파일 저장할 수 있는 imageField
    head_image = models.ImageField(upload_to='artwork/images/%Y/%M/%d/', blank=True)

    author = models.ForeignKey(User,on_delete=models.CASCADE) # 다대일관계
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL) # 다대일 관계
    tags = models.ManyToManyField(Tag, blank=True) # 다대다관계
    commericial = models.CharField(max_length=100) # 상업/비상업

    def __str__(self):
        return f'[{self.pk}]{self.title} :: {self.author}'

    def get_absolute_url(self): # 상세 포스트주소
        return f'/artwork/{self.pk}'

    def get_description_markdown(self):
        return markdown(self.description) # 기존텍스트 html를 마크다운 형식으로 변경