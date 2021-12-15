from django.contrib import admin
from .models import Work, Category

# Register your models here.
admin.site.register(Work)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)} # slug 값 넣어줌.
admin.site.register(Category, CategoryAdmin)