# = views_DP
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
   path('admin/', admin.site.urls), # path to the admin page
   path('pages/', include('django.contrib.flatpages.urls')),  # < Подключаем представления
   path('posts/', include('news.urls')),  # < Подключаем представления сначала в news\urls.py находим  PostsList.as_view, => views.py template_name = 'posts.html'
]

# /news/create/
# /news/<int:pk>/edit/
# /news/<int:pk>/delete/
# /articles/create/
# /articles/<int:pk>/edit/
# /articles/<int:pk>/delete/