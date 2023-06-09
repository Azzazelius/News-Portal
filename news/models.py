from django.core.mail import send_mail
from django.db import models
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse


class Author(models.Model):
    full_name = models.CharField(max_length=100)
    rating = models.IntegerField(default=0) # значение вычисляется в update_rating
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE) # связь с методом User один к одному

    def update_rating(self):
        r_comments_by_author = Comment.objects.filter(user_id=self.user.id).aggregate(models.Sum('rating'))['rating__sum'] # new variant

        r_posts = Post.objects.filter(author_id=self).aggregate(models.Sum('rating')) #суммарный рейтинг за посты
        post_ids = Post.objects.filter(author_id=self).values_list('id', flat=True) #(flat=True) чтобы получить одним списком id всех постов этого автора
        r_comments_to_author_posts = Comment.objects.filter(post_id__in=post_ids).aggregate(models.Sum('rating'))['rating__sum']

        print(r_posts, r_posts['rating__sum'], r_comments_by_author, r_comments_to_author_posts)
        self.rating = (int(r_posts['rating__sum']) * 3) + int(r_comments_by_author) + int(r_comments_to_author_posts)
        print(self.rating)
        self.save()

    def __str__(self):
        return self.full_name


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField('auth.user', blank=True, related_name='subscribers', verbose_name='подписчики')

    def __str__(self):
        return self.category_name


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
    rating = models.IntegerField(default=0, db_column='rating')

    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='post')
    category = models.ManyToManyField('Category', blank=True, through='PostCategory', verbose_name='Категории')  # Связь многие к многим

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        content = self.content[:124]
        if len(self.content) > 124:
            content += '...'
        return content

    def get_absolute_url(self):
        return reverse('post_full', args=[str(self.id)])



class PostCategory(models.Model): # Промежуточная модель для связи «многие ко многим»:
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)


class Comment(models.Model):
    comment = models.TextField(max_length=500)
    t_creation = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0, db_column='rating')  #рейтинг самого комментария

    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return self.comment


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:  # Отправляем письмо только при создании нового пользователя
        subject = 'Welcome to Our Site!'
        message = render_to_string('welcome_email.html', {'user': instance})
        from_email = 'Pupapekainos@yandex.com'
        recipient_list = [instance.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False, html_message=message)
