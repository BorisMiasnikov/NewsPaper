from django import forms
from django.core.exceptions import ValidationError

from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            # 'author',
            'title',
            'text',
            'category',
        ]
        labels = {
            # 'author': 'Автор',
            'title':'Заголовок',
            'text': 'Содержание',
            'category': 'Категория',
        }
        widgets = {
            'title': forms.Textarea(attrs={'class':'form-text', 'cols':70, 'rows':3}),
            'text': forms.Textarea(attrs={'class': 'form-text', 'cols': 70, 'rows': 10}),
        }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        text = cleaned_data.get('text')
        if title is not None and len(title) < 10:
            raise ValidationError({
                "title": "Заголовок не может быть меньше 10 имволов"
            })
        if text == title:
            raise ValidationError("Заголовок не может быть идентичен содержанию")
        return cleaned_data