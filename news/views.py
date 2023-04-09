# Импортируем класс, который говорит нам о том,что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView
from .models import Author, Category, Post, Comment
from datetime import datetime
from pprint import pprint


class PostsList(ListView):
    model = Post # Указываем модель, объекты которой мы будем выводить
    ''' ordering = '' Заметка. Тут надо добавить сортировку по времени'''
    # queryset = .objects.filter # опциональный фильтр, на случай если ещё пригодится
    template_name = 'posts.html'  # Указываем имя шаблона, с инструкциями по отображению объектов модели
    context_object_name = 'posts'  # Это имя списка где лежат все объекты. К нему обращаемся в html-шаблоне.

class PostFull(DetailView):
    model = Post
    template_name = 'post_full.html'
    context_object_name = 'post'


    # def get_context_data(self, **kwargs): # Метод get_context_data позволяет нам изменить набор данных,который будет передан в шаблон.
    #     # С помощью super() мы обращаемся к родительским классам
    #     # и вызываем у них метод get_context_data с теми же аргументами,
    #     # что и были переданы нам.
    #     # В ответе мы должны получить словарь.
    #     #
    #     # Отвечает за вывод информации в словаре темплейта.
    #     # Например {{ product }} в product.html. Он наследуется из класса ListView.
    #     # Но можно изменить его функционал прописав его в методе. Как показано ниже
    #     context = super().get_context_data(**kwargs)
    #     # К словарю добавим текущую дату в ключ 'time_now'.
    #     context['time_now'] = datetime.utcnow()
    #     # Добавим ещё одну пустую переменную,
    #     # чтобы на её примере рассмотреть работу ещё одного фильтра.
    #     context['next_sale'] = None
    #     pprint(context)
    #     return context
    #