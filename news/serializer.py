from .models import *
from rest_framework import serializers

class PostCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PostCategory
        fields = ['category'] # только это поле, потому что связи с постом еще не существует

class PostSerializer(serializers.HyperlinkedModelSerializer):
    categories = PostCategorySerializer(many=True)
    rating = serializers.FloatField(read_only= True)
    data_in = serializers.DateTimeField(format= '%d-%m-%Y %H:%M:%S', read_only= True)
    class Meta:
        model = Post
        fields = ['id', 'author', 'category', 'title', 'text', 'choice_field', 'data_in', 'rating', 'categories'] # categories - это релейтид нейм из модели посткатегори


class NewsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'category', 'title', 'text', 'choice_field']


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'category', 'title', 'text', 'choice_field']

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    # category = serializers.CharField(source= 'get_name_of_category_display')
    class Meta:
        model = Category
        fields = ['id', 'category']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']






