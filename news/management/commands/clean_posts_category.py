from django.core.management.base import BaseCommand

from news.models import PostCategory, Category, Post


class Command(BaseCommand):
    help = 'Удаляет все посты вбранной категории'
    #requires_migrations_checks = True #напоминание о выполнении миграций, если таковые есть
    post_category = ", ".join([cat.category for cat in Category.objects.all()]) #Собираем кверисет всех категорий

    def handle(self, *args, **options):
        #self.stdout.readable()#не понятно что делает, скопировал из урока
        self.stdout.write(f'Введите имя категории, в которой удалить все посты: {self.post_category}')#Выводит это сообщение и добавляет все категории
        category = input() #вводим категорию
        try:
            category = Category.objects.get(category=category)#находим все записи с этой категорией
            self.stdout.write('Действительно хотите удалить ввсе посты? yes/no')
            answer = input()  # считываем подтверждение
            if answer != 'yes':
                self.stdout.write(self.style.ERROR('Отменено'))
                return
            else:
                Post.objects.filter(category__category=category).delete()
                self.stdout.write(self.style.SUCCESS(f'Успешно удалены все публикации из категории {category}'))
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