from django.contrib import admin
from .models import Work, Category, Tag, Comment
from markdownx.admin import MarkdownxModelAdmin

# Register your models here.
admin.site.register(Work, MarkdownxModelAdmin)
admin.site.register(Comment)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)} # slug 값 넣어줌.

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag,TagAdmin)