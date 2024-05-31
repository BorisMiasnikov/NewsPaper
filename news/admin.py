from django.contrib import admin
from .models import Post, Author, Comment, Category
from modeltranslation.admin import TranslationAdmin #импортируем модель админки (нужно так же обновить в памяти из модуль
#про переопределение стандартных админ инструментов

def nullfy_rating(modeladmin, request, queryset):#функция обнуления рейтинга
    #request — объект хранящий информацию о запросе и queryset — грубо говоря набор объектов, которых мы выделили галочками.
    queryset.update(rating=0)
    nullfy_rating.short_description = 'Обнулить рейтинг'  # описание для более понятного представления в админ панеле задаётся, как будто это объект

class PostAdmin(admin.ModelAdmin):# создаём новый класс для представления товаров в админке
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ['title', 'data_in', 'rating', 'author', 'categories' ]
    list_filter = ('author', 'data_in', 'category')#добавляем примитивные фильтры
    search_fields = ('title', 'category__category' )
    actions = [nullfy_rating]


    def categories(self, obj):
        return ", ".join(cat.category for cat in obj.category.all())

# Регистрируем модели для перевода в админке
class TransCategoryAdmin(TranslationAdmin):
    model = Category

class TransPostAdmin(PostAdmin, TranslationAdmin):
    model = Post



admin.site.register(Post, TransPostAdmin)#регистрация транспостадмин включает в себя пост админ
admin.site.register(Author)
admin.site.register(Category, TransCategoryAdmin)
admin.site.register(Comment)

