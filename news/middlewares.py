import pytz #импортируем стандартный модуль для работы с поясами часовыми
from django.utils import timezone

class TimezoneMiddlware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tzname = request.session.get('django_timezone')# пытаемся забрать часовой пояс из сессии
        # если он есть в сессии , то выставляем такой часовой пояс. Если его нет, значит он не установлен, и часовой
        # пояс надо выставить по умолчанию (на время сервера)
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
        return self.get_response(request)