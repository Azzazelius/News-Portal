# Импортируем класс, который говорит нам о том,что в этом представлении мы будем выводить список объектов из БД
from django.urls import reverse_lazy
from django.views.generic import (
                                    ListView,
                                    DetailView,
                                    CreateView,
                                    UpdateView,
                                    DeleteView,
                                    RedirectView,
                                    TemplateView
                                )
from .models import (Post, Author, Category, Comment)
from .forms import NewsForm, SubscribeForm
from .filters import PostFilter, CategoryFilter
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, render
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMultiAlternatives

from django.template.loader import render_to_string  # импортируем функцию, которая срендерит наш html в текст
from datetime import datetime


class HomePageView(RedirectView):
    url = 'posts/'
    permanent = True


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
                                                                 # Сохраняем нашу фильтрацию в объекте класса, чтобы потом добавить в контекст и использовать в шаблоне.
        return self.filterset.qs  # Возвращаем из функции отфильтрованный список товаров

    def get_context_data(self, **kwargs):  # Метод get_context_data позволяет нам изменить набор данных, который будет передан в шаблон.
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset  # Добавляем в контекст объект фильтрации.
        context['post_count'] = Post.objects.count()
        return context


class PostFull(DetailView):
    model = Post
    template_name = 'post_full.html'
    context_object_name = 'post'


class NewsCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'news.add_post'
    form_class = NewsForm
    model = Post
    template_name = 'create.html'
    success_url = reverse_lazy('posts_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        news_notify = NewsSendNotify()
        news_notify.notify(self.object)
        return response


# Класс отпавки нотификации
class NewsSendNotify:
    @staticmethod
    def notify(post):
        categories = post.category.all() # создаём список всех категорий в новости
        recipient_list = []
        for category in categories:  # цикл проходит по каждой категории, собирая информацию о подписчиках,
                                     # складывая их емейлы в recipient_list
            subscribers = category.subscribers.all()
            recipient_list += [user.email for user in subscribers]

        if recipient_list:
            subject = f'Новый пост в категориях "{", ".join([str(category) for category in categories])}"'
            message = f'Появился новый пост в категориях "{", ".join([str(category) for category in categories])}"\n{post.content[:50]}'
            html = render_to_string('news_email.html', {'post': post})
            from_email = 'Pupapekainos@yandex.com'
            msg = EmailMultiAlternatives(subject, message, from_email, recipient_list)
            msg.attach_alternative(html, "text/html")
            msg.send()


class NewsEdit(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'news.change_post'
    form_class = NewsForm
    model = Post
    template_name = 'create.html'
    success_url = reverse_lazy('posts_list')

    def form_valid(self, form):   # этот метод тут только для тестирования, менять новость быстрее, чем создавать
        response = super().form_valid(form)
        news_notify = NewsSendNotify()
        news_notify.notify(self.object)
        return response


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'news.delete_post'
    model = Post
    template_name = 'delete.html'
    success_url = reverse_lazy('posts_list')


class PostSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'
    success_url = reverse_lazy('posts_list')

    def get_queryset(self):
        queryset = super().get_queryset()  # Получаем обычный запрос
        # Используем наш класс фильтрации. self.request.GET содержит объект QueryDict,
        # который мы рассматривали в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса, чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class IndexView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context


class SubscribeView(TemplateView):
    model = Category
    form_class = SubscribeForm
    template_name = 'subscribe.html'
    context_object_name = 'subscribe'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = CategoryFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filterset = CategoryFilter(self.request.GET, queryset=Category.objects.all())
        context['filterset'] = filterset
        return context


    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            # process form data
            return redirect('../')
        return render(request, self.template_name, {'form': form})


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')




# Пока не используется. Запланированно на раздельный вывод новостей и статей
#
# class ArticlesList(ListView):
#     model = Post  # Указываем модель, объекты которой мы будем выводить
#     # ordering = '-t_creation'  # Заметка. Тут надо добавить сортировку по времени
#     queryset = Post.objects.filter(post_type='ar') # опциональный фильтр, на случай если ещё пригодится
#     template_name = 'posts/articles.html'  # Указываем имя шаблона, с инструкциями по отображению объектов модели
#     context_object_name = 'articles'  # Это имя списка где лежат все объекты. К нему обращаемся в html-шаблоне.



    # Код оставшийся с одной из реализациq вьюхи подписки. Не удаляю, что бы помнить, что такое уже пробовал
    #
    # def form_valid(self, form):
    #     user = self.request.user
    #     categories = form.cleaned_data.get('categories')
    #     for category in categories:
    #         category.subscribers.add(user)
    #     return redirect('subscribe-success')


# Заметки на оповешение манагеров
# ---------------------------
# def notify_managers_appointment(sender, instance, created, **kwargs):
#     subject = f'{instance.client_name} {instance.date.strftime("%d %m %Y")}'
#
#     mail_managers(
#         subject=subject,
#         message=instance.message,
#     )
#

