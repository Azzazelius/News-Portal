from django.contrib import admin
from .models import Author, Category, Post, Comment


# напишем уже знакомую нам функцию обнуления товара на складе
def rename_title(modeladmin, request, queryset): # все аргументы уже должны быть вам знакомы, самые нужные из них это request — объект хранящий информацию о запросе и queryset — грубо говоря набор объектов, которых мы выделили галочками.
    queryset.update(title="test")
rename_title.short_description = 'Переименовать заголовок' # описание для более понятного представления в админ панеле задаётся, как будто это объект

# создаём новый класс для представления постов в админке
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "rating", "t_creation")
    list_filter = ("rating", "t_creation")
    search_fields = ["title"]
    actions = [rename_title]


# Тут регистрируем модели, иначе мы не увидим их в админке.
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)

