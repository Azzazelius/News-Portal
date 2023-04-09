# = simpleapp
from django.urls import path
from .views import PostsList, PostFull

urlpatterns = [
   path('', PostsList.as_view()),
   path('<int:pk>', PostFull.as_view()),
]
