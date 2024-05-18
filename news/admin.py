from django.contrib import admin
from .models import Post, Author, Comment, Category

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

admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Comment)

