from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path('', views.home, name='home'),
]
