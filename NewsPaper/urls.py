from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views


urlpatterns = [
   path('admin/', admin.site.urls), # path to the admin page
   path('pages/', include('django.contrib.flatpages.urls')),  # < Подключаем представления
   path('posts/', include('news.urls')),  # < Подключаем представления сначала в news\urls.py находим  PostsList.as_view, => views.py template_name = 'posts.html'
   path('accounts/', include('django.contrib.auth.urls')),
   path('accounts/social/', include('allauth.urls')),
   path('', TemplateView.as_view(template_name='homepage.html'), name='home'),

]



# /news/create/
# /news/<int:pk>/edit/
# /news/<int:pk>/delete/
# /articles/create/
# /articles/<int:pk>/edit/
# /articles/<int:pk>/delete/