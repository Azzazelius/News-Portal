# Импортируем класс, который говорит нам о том,что в этом представлении мы будем выводить список объектов из БД
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import (Author, Category, Post, Comment)
from .forms import NewsForm
from .filters import PostFilter



class PostsList(ListView):
    model = Post # Указываем модель, объекты которой мы будем выводить
    # ordering = 't_creation' # Заметка. Тут надо добавить сортировку по времени
    ordering = '-t_creation' # Заметка. Тут надо добавить сортировку по времени
    # queryset = .objects.filter # опциональный фильтр, на случай если ещё пригодится
    template_name = 'posts.html'  # Указываем имя шаблона, с инструкциями по отображению объектов модели
    context_object_name = 'posts'  # Это имя списка где лежат все объекты. К нему обращаемся в html-шаблоне.
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()  # Получаем обычный запрос
        self.filterset = PostFilter(self.request.GET, queryset)  # Используем наш класс фильтрации. self.request.GET содержит объект QueryDict,
                                                                 # который мы рассматривали в этом юните ранее.
                                                                 # Сохраняем нашу фильтрацию в объекте класса, чтобы потом добавить в контекст и использовать в шаблоне.
        return self.filterset.qs  # Возвращаем из функции отфильтрованный список товаров

    def get_context_data(self, **kwargs):  # Метод get_context_data позволяет нам изменить набор данных, который будет передан в шаблон.
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset  # Добавляем в контекст объект фильтрации.
        return context


class PostFull(DetailView):
    model = Post
    template_name = 'post_full.html'
    context_object_name = 'post'


class ArticlesList(ListView):
    model = Post  # Указываем модель, объекты которой мы будем выводить
    # ordering = '-t_creation'  # Заметка. Тут надо добавить сортировку по времени
    queryset = Post.objects.filter(post_type='ar') # опциональный фильтр, на случай если ещё пригодится
    template_name = 'posts/articles.html'  # Указываем имя шаблона, с инструкциями по отображению объектов модели
    context_object_name = 'articles'  # Это имя списка где лежат все объекты. К нему обращаемся в html-шаблоне.


class NewsCreate(CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'create.html'
    success_url = reverse_lazy('posts_list')


class NewsEdit(UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'create.html'
    success_url = reverse_lazy('posts_list')


class NewsDelete(DeleteView):
    # form_class = NewsForm
    model = Post
    template_name = 'delete.html'
    success_url = reverse_lazy('posts_list')


class PostSearch(ListView):
    model = Post # Указываем модель, объекты которой мы будем выводить
    template_name = 'search.html'  # Указываем имя шаблона, с инструкциями по отображению объектов модели
    context_object_name = 'posts'  # Это имя списка где лежат все объекты. К нему обращаемся в html-шаблоне.

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации. self.request.GET содержит объект QueryDict, который мы рассматривали в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса, чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

   # Метод get_context_data позволяет нам изменить набор данных, который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context