from django.core.management.base import BaseCommand

from news.models import PostCategory

class Command(BaseCommand):
    help = 'Удаляет все посты вбранной категории'
    requires_migrations_checks = True #напоминание о выполнении миграций, если таковые есть
    post_category = PostCategory.objects.all() #Собираем кверисет всех категорий

    def handle(self, *args, **options):
        self.stdout.readable()#не понятно что делает, скопировал из урока
        self.stdout.write('Введите имя категории, в которой удалить все посты "%s"' % cat for cat in post_category )#Выводит это сообщение и добавляет все категории
        category = input() #вводим категорию
        try:
            for cat in post_category: #проходим по всем категориям
                if cat.category.category == category: #сравниваем с введеной
                    self.stdout.readable() #опять не понятно что делает
                    self.stdout.write('Действительно хотите удались все посты? yes/no')  # спрашиваем пользователя, действительно ли он хочет удалить все товары
                    answer = input()  # считываем подтверждение
                    if answer == 'yes':
                        cat.post.delete() #удаляем посты выбранной категории
                        self.stdout.write(self.style.SUCCESS('Введите имя категории, в которой удалить все посты "%s"' % cat for cat in post_category))
                    return
        except PostCategory.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Не существует категории {category}'))

# Альтернатива
# from django.core.management.base import BaseCommand, CommandError
# from sample_app.models import Product, Category
#
#
# class Command(BaseCommand):
#     help = 'Подсказка вашей команды'
#
#     def add_arguments(self, parser):
#         parser.add_argument('category', type=str)
#
#     def handle(self, *args, **options):
#         answer = input(f'Вы правда хотите удалить все статьи в категории {options["category"]}? yes/no')
#
#         if answer != 'yes':
#             self.stdout.write(self.style.ERROR('Отменено'))
#             return
#         try:
#             category = Category.objects.get(name=options['category'])
#             Post.objects.filter(category=category).delete()
#             self.stdout.write(self.style.SUCCESS(f'Succesfully deleted all news from category {category.name}')) # в случае неправильного подтверждения говорим, что в доступе отказано
#         except Post.DoesNotExist:
#             self.stdout.write(self.style.ERROR(f'Could not find category {}'))