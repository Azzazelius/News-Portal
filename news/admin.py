from django.contrib import admin
from .models import Author, Category, Post, Comment

# Тут регистрируем модели, иначе мы не увидим их в админке.
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
