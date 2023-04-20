# = simpleapp
from django.urls import path
from .views import PostsList, PostFull, NewsEdit, NewsCreate, NewsDelete, PostSearch
from .views import upgrade_me


urlpatterns = [
   path('', PostsList.as_view(), name='posts_list'),
   path('<int:pk>/', PostFull.as_view(), name='post_full'),
   path('<int:pk>/edit/', NewsEdit.as_view(), name='news_edit'),
   path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('create/', NewsCreate.as_view(), name='news_create'),
   path('search/', PostSearch.as_view(), name='news_search'),
   path('upgrade/', upgrade_me, name='upgrade'),
   # path('mailing/', MailingView.as_view('post'), name='mailing'),
]
