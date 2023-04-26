# Реализовать рассылку уведомлений подписчикам после создания новости.
# Реализовать еженедельную рассылку с последними новостями (каждый понедельник в 8:00 утра).
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .models import Post, Category
from celery import shared_task
from django.urls import reverse_lazy

@shared_task
def notify(post_id):
    post = Post.objects.get(id=post_id)
    categories = post.category.all()
    recipient_list = []
    for category in categories:
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

# ↓↓↓↓Предыдущий вариант реализации. Его можно удалить если работает вариант выше.↓↓↓↓
# @shared_task
# def send_notifications(post_id):
#     post = Post.objects.get(id=post_id)
#     categories = post.category.all()  # создаём список всех категорий в новости
#     subscribers = Category.subscribers.objects.all()
#     subject = post.title
#     message = post.content
#
#     from_email = 'your_email@gmail.com'
#     recipient_list = [subscriber.email for subscriber in subscribers]
#     send_mail(subject, message, from_email, recipient_list)
#
#     @staticmethod
#     def notify(post):
#         categories = post.category.all() # создаём список всех категорий в новости
#         recipient_list = []
#         for category in categories:  # цикл проходит по каждой категории, собирая информацию о подписчиках,
#                                      # складывая их емейлы в recipient_list
#             subscribers = category.subscribers.all()
#             recipient_list += [user.email for user in subscribers]
#
#         if recipient_list:
#             subject = f'Новый пост в категориях "{", ".join([str(category) for category in categories])}"'
#             message = f'Появился новый пост в категориях "{", ".join([str(category) for category in categories])}"\n{post.content[:50]}'
#             html = render_to_string('news_email.html', {'post': post})
#             from_email = 'Pupapekainos@yandex.com'
#             msg = EmailMultiAlternatives(subject, message, from_email, recipient_list)
#             msg.attach_alternative(html, "text/html")
#             msg.send()