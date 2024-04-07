from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.core.mail import send_mail

from NewsPaper import settings


class CommonSignupForm(SignupForm):

    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        #     subject=f'Добро пожаловать',  # имя клиента и дата записи будут в теме для удобства
        #     message='Авторизация на сайте прошла успешно',  # сообщение с кратким описанием проблемы
        #     from_email=settings.DEFAULT_FROM_EMAIL, # здесь указываете почту, с которой будете отправлять (об этом попозже)
        #     recipient_list=user.email  # здесь список получателей. Например, секретарь, сам врач и т. д.
        # )
        return user