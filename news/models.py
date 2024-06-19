from django.core.cache import cache
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext as _
from django.utils.translation import pgettext_lazy # импортируем «ленивый» геттекст с подсказкой



class Author(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        post_rating = 0
        user_comments_rating = 0
        post_comments_rating = 0

        post = Post.objects.filter(author= self)
        for p in post:
            post_rating += p.rating

        user_comments = Comment.objects.filter(user = self.user)
        for u in user_comments:
            user_comments_rating += u.rating

        post_comments = Comment.objects.filter(post__author = self)
        for pc in post_comments:
            post_comments_rating += pc.rating

        self.rating = post_rating * 3 + user_comments_rating + post_comments_rating
        self.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    category = models.TextField(unique=True, help_text=_('Category!')) #добавил хелп текст, что бы проверить перевод в админ панели
    subscriber = models.ManyToManyField(User, related_name="categories")

    def __str__(self):
        return f'{self.category.title()}'


class Post(models.Model):

    news = "N"
    article = "A"

    POSITIONS = [(news, "Новость"), (article, "Статья")]

    author = models.ForeignKey(Author, on_delete= models.CASCADE)
    choice_field = models.CharField(max_length= 1, choices=POSITIONS, default=article)
    data_in = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through="PostCategory")
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=3000)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:125] + "..."

    def __str__(self):
        return f'{self.title.title()}: {self.preview()}'

    def get_absolute_url(self):#это абсолютный путь, что бы после зоздания перебрасывало на страницу с товаром
        return reverse('Post_detail', args= [str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name= 'categories')
    category = models.ForeignKey(Category, on_delete= models.CASCADE, related_name= 'posts')


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete= models.CASCADE)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    text = models.CharField(max_length=1000)
    data_in = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()



