from django.shortcuts import render
from rest_framework import viewsets, permissions

from .serializer import *
from .models import *

class PostViewset(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AuthorViewset(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class NewsViewset(viewsets.ModelViewSet):
    queryset = Post.objects.filter(choice_field = 'N')
    serializer_class = NewsSerializer


class ArticleViewset(viewsets.ModelViewSet):
    queryset = Post.objects.filter(choice_field = 'A')
    serializer_class = ArticleSerializer
