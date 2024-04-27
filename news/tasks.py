from celery import shared_task
import time
from datetime import datetime, date, timedelta

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from NewsPaper import settings
from news.models import Category, Post


@shared_task
def hello():
    time.sleep(10)
    print("Hello")

@shared_task
def printer(N):
    for i in range(N):
        time.sleep(1)
        print(i+1)
        print(timezone.now() + timedelta(seconds=5))

#ниже отправка статей за неделю. Сперва нужно закомментировать отравку такую же в runapschedular, чтоб не дублировалось
@shared_task
def sending_posts_past_week():
    today = datetime.now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(data_in__gte=last_week)
    categories = set(posts.values_list("category__category", flat=True))
    subscribers = set(Category.objects.filter(category__in=categories).values_list("subscriber__email", flat=True))
    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()

#ниже отправка имейла при добавлении новости. это идет взамен сигналов, в сигналах эти функции нужно закомментировать
@shared_task
def notification_new_post(pk):
    post = Post.objects.get(pk=pk)
    preview = post.preview()
    title = post.title
    categories = post.category.all()
    subscribers_email = []
    for category in categories:
        users = category.subscriber.all()
        for user in users:
            subscribers_email.append(user.email)

    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/posts/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_email
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()