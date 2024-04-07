from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, TemplateView

from sign.views import authors_in

# from .views import BaseRegisterView

urlpatterns = [
    path('login/', LoginView.as_view(template_name = 'login.html'), name= 'login'),
    path('logout/', LogoutView.as_view(template_name= 'logout.html'), name= 'logout'),
    path('logout_confirm/', TemplateView.as_view(template_name='logout_confirm.html'), name='logout_confirm'),
    # path('signup/', BaseRegisterView.as_view(template_name='signup.html'), name='signup'),
    path('authors_in/', authors_in, name='authors_in'),

]