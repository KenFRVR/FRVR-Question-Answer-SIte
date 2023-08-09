from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('login', views.Login.as_view(), name='login'),
    path('register/', views.Register.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('create-question/', views.CreateQuestion.as_view(), name='create-question'),
    path('edit-question/', views.EditQuestion.as_view(), name='edit-question')
]
