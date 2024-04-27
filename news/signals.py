# from django.conf import settings
# from django.core.mail import EmailMultiAlternatives, mail_managers
# from django.db.models.signals import m2m_changed, pre_delete
# from django.dispatch import receiver
# from django.template.loader import render_to_string
#
# from news.models import PostCategory, Post
#
#
# def send_notifications(preview, pk, title, subscribers):
#     html_content = render_to_string(
#         'post_created_email.html',
#         {
#             'text': preview,
#             'link': f'{settings.SITE_URL}/posts/{pk}'
#         }
#     )
#
#     msg = EmailMultiAlternatives(
#         subject=title,
#         body='',
#         from_email= settings.DEFAULT_FROM_EMAIL,
#         to=subscribers
#     )
#
#     msg.attach_alternative(html_content, 'text/html')
#     msg.send()
#
#
# def send_notifications_delete(text, subscribers):
#     html_content = render_to_string(
#         'post_delete_email.html',
#         {
#             'text': text,
#         }
#     )
#
#     msg = EmailMultiAlternatives(
#         subject='delete',
#         body='',
#         from_email= settings.DEFAULT_FROM_EMAIL,
#         to=subscribers
#     )
#
#     msg.attach_alternative(html_content, 'text/html')
#     msg.send()
#
#
# @receiver(m2m_changed, sender = PostCategory)
# def notify_about_new_post(sender, instance, **kwargs):
#     if kwargs['action'] == 'post_add':
#         category = instance.category.all()
#         subscribers_emails = []
#
#         for cat in category:
#             subscribers = cat.subscriber.all()
#             subscribers_emails += [s.email for s in subscribers]
#
#         send_notifications(instance.preview(), instance.pk, instance.title, subscribers_emails)
#
# @receiver(pre_delete, sender = Post)
# def notify_about_delete_post(sender, instance, **kwargs):
#     subscribers_emails = []
#     categories = instance.category.all()
#     for cat in categories:
#         subscribers = cat.subscriber.all()
#         subscribers_emails += [user.email for user in subscribers]
#
#     subject =  f'в вашей любимой категории стало на 1 постик меньше'
#     send_notifications_delete(subject, subscribers_emails)
#
#
#
