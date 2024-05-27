from datetime import datetime, date, timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.cache import cache

from .filters import PostFilter
from .models import Post, Category
from .forms import PostForm

from .tasks import hello, printer, notification_new_post

from django.utils.translation import gettext as _


class PostsList(ListView):
    model = Post
    ordering = '-data_in'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context



class PostsSearch(ListView):
    model = Post
    ordering = '-data_in'
    template_name = 'posts_search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    #добавляем кеширование страницы с новостью
    def get_object(self, *args, **kwargs):# переопределяем метод получения объекта, как ни странно
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)# кэш очень похож на словарь, и метод get действует так же. Он забирает значение по ключу, если его нет, то забирает None.
        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj

class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.choice_field = 'N'
        post.author = self.request.user.author
        today = date.today()
        post_limit = Post.objects.filter(author= post.author, data_in__date=today).count()
        if post_limit >=3:
            return render(self.request, template_name='post_limit.html', context={'author': post.author})
        post.save()
        # notification_new_post.apply_async([post.pk]) #добавил отправку сообщения о создании, передал первичнй ключ
        return super().form_valid(form)



class ArticlesCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'articles_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.choice_field = 'A'
        post.author = self.request.user.author
        today = date.today()
        post_limit = Post.objects.filter(author= post.author, data_in__date=today).count()
        if post_limit >=3:
            return render(self.request, template_name='post_limit.html', context={'author': post.author})
        post.save()
        notification_new_post.apply_async([post.pk]) #добавил отправку сообщения о создании, передал первичнй ключ
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('Posts_list')


class CategoriesPostList(PostsList):
    model = Post
    template_name = "category_list.html"
    context_object_name = "category_news_list"

    def get_queryset(self):
        self.category = get_object_or_404(Category, id = self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-data_in')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscribers'] = self.request.user not in self.category.subscriber.all()
        context['category'] = self.category
        context['subscribe'] = _('Subscribe')#создали эту переменную, что б перевести ее через gettext() _() на en и она вставляется в html в виде {{ subscribe }}
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscriber.add(user)

    massage = 'Это успешная подписка на'
    return render(request, 'subscriber.html', {'category':category, 'massage':massage})

# это пример из модуля реализация apply_async
class IndexView(View):
    def get(self, request):
        printer.apply_async([10], eta = timezone.now() + timedelta(seconds=5)) #это метод apply_async(args[, kwargs[, ...]])
        hello.delay() #это метод   delay(*args, **kwargs). это сокращение от первого
        return HttpResponse("Hello!")


