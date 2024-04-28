from django.urls import path

from django.views.decorators.cache import cache_page

# Импортируем созданное нами представление
from .views import PostsList, PostDetail, PostsSearch, NewsCreate, PostUpdate, PostDelete, ArticlesCreate, \
    CategoriesPostList, subscribe, IndexView

urlpatterns = [
    path('', cache_page(60)(PostsList.as_view()), name= 'Posts_list'),
    path('<int:pk>/', cache_page(300)(PostDetail.as_view()), name= 'Post_detail'),
    path('search/', PostsSearch.as_view(), name= 'Posts_search'),
    path('news/create/', cache_page(1000)(NewsCreate.as_view()), name='News_create'),
    path('news/<int:pk>/edit/', PostUpdate.as_view(), name='News_edit'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='News_delete'),
    path('articles/create/', cache_page(1000)(ArticlesCreate.as_view()), name='Articles_create'),
    path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='Articles_edit'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='Articles_delete'),
    path('categories/<int:pk>/', cache_page(60)(CategoriesPostList.as_view()), name='Category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='Subscribe'),
    path('hello',IndexView.as_view()), #эта страница для проверки работы IndexView
]