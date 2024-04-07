import django_filters
from django_filters import FilterSet, DateFilter
from django import forms

from .models import Post

class PostFilter(FilterSet):
    data_in = DateFilter(field_name='data_in',
                         widget=forms.DateInput(attrs={'type': 'date'}),
                         label='Дата',
                         lookup_expr='date__gte',
                         )
    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'author': ['exact'],
        }
