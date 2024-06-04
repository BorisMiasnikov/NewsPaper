from django.shortcuts import render
from rest_framework import viewsets, permissions

from .serializer import *
from .models import *

class PostViewset(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

