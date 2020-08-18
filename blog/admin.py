from django.contrib import admin
from .models import Category, Post, Comment

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}




admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Category, CategoryAdmin)