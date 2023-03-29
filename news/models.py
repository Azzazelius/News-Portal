from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Author(models.Model):
    full_name = models.CharField(max_length=100)
    rating = models.FloatField(default=0) # значение вычисляется в update_rating
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE) # связь с методом User один к одному

    def update_rating(self):
        post_ids = self.post.set.filter(author=self).values_list('id', flat=True) #получаем одним списком (flat=True) id всех постов этого автора
        r_posts = Post.objects.filter(author=self).aggregate(models.Sum('rating'))
        r_posts_sum = r_posts['rating__sum'] if r_posts and len(r_posts) == 1 else 0
        r_author_comments = Comment.objects.filter(post__author=self).aggregate(models.Sum('rating'))['rating__sum'] # Аналогично строке выше. Но, двойным "_" (post__author=self) указываем, что интересующий нас параметр author находится не в таблице comments, а в связаной с ней таблицей post
        r_posts_comments = Comment.objects.filter(post__id__in=post_ids).aggregate(models.Sum('rating'))['rating__sum']
        self.rating = r_posts_sum * 3 + r_author_comments + r_posts_comments
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    ar = 'Article'
    nw = 'News'

    post_types = [
        (ar, 'Article'),
        (nw, 'News')
    ]

    post_type = models.CharField(max_length=7, choices=post_types, default=nw)
    t_creation = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    _rating = models.FloatField(default=0.0, db_column='rating')

    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='post')
    category = models.ManyToManyField('Category', through='PostCategory') # Связь многие к многим

    @property # геттер рейтинга поста
    def rating(self):
        return self._rating

    @rating.setter
    def like(self):
        self._rating += 1
        self.save(update_fields=['_rating'])

    @rating.setter
    def dislike(self):
        self._rating -= 1 # рейтинг может быть отрицательным
        self.save(update_fields=['_rating'])

    def preview(self):
        content = self.content[:124]
        if len(self.content) > 124:
            content += '...'
        return content

class PostCategory(models.Model): # Промежуточная модель для связи «многие ко многим»:
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)



class Comment(models.Model):
    comment = models.TextField(max_length=500)
    t_creation = models.DateTimeField(auto_now_add=True)
    _rating = models.FloatField(default=0.0, db_column='rating') #рейтинг самого комментария

    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)


    @property  # геттер рейтинга поста
    def rating(self):
        return self._rating

    @rating.setter
    def like(self):
        self._rating += 1
        self.save(update_fields=['_rating'])

    @rating.setter
    def dislike(self):
        self._rating -= 1  # рейтинг может быть отрицательным
        self.save(update_fields=['_rating'])

# ===========================
