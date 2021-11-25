from django.db import models

# Create your models here.

class Work(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    price = models.CharField(max_length=100)
    # author
    # category
    # tags
    commericial = models.CharField(max_length=100)

    #thumnail = models.ImageField(upload_to='artworks/images/%Y/%M/%d/', blank=True)

    def __str__(self):
        return f'[{self.pk}]{self.title}'

    def get_absolute_url(self): # 상세 포스트주소
        return f'/artwork/{self.pk}'