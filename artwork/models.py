from django.db import models

# Create your models here.

class Work(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.CharField(max_length=100)

    # 이미지 파일 저장할 수 있는 imageField
    head_image = models.ImageField(upload_to='artwork/images/%Y/%M/%d/', blank=True)

    # author
    # category
    # tags
    commericial = models.CharField(max_length=100) # 상업/비상업


    def __str__(self):
        return f'[{self.pk}]{self.title}'

    def get_absolute_url(self): # 상세 포스트주소
        return f'/artwork/{self.pk}'