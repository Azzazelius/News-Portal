from django.test import TestCase

# Create your tests here.

from django.contrib.auth.models import User
from django.db.models import Max
from news.models import Author
from news.models import Category
from news.models import Post
from news.models import Comment

