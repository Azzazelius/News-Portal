from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .models import User, Post, Category
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


@shared_task
def weekly_notify():
    from .views import WeeklyPostsView
    recipient_list = User.objects.values_list('email', flat=True)  # список емейлов всех пользователей

    if recipient_list:  # рассылка отправляется только если есть хотя бы один адресат
        queryset = WeeklyPostsView().get_queryset()  # get the queryset for the view
        if queryset.exists():
            subject = f'Еженедельный дайджест'
            message = f'Список новостей за прошедшую неделю'
            from_email = 'Pupapekainos@yandex.com'
            context = {'posts': queryset, 'request': None, 'filter': WeeklyPostsView().filterset_class}  # pass the posts and request object to the email template context
            html_content = render_to_string('weekly_posts_email.html', context)
            msg = EmailMultiAlternatives(subject, message, from_email, recipient_list)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

