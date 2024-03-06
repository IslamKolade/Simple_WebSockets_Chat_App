from django.urls import path
from . import views

urlpatterns = [
    path("join_chat/", views.join_chat, name="join_chat"),
    path("create_chat/", views.create_chat, name="create_chat"),
    path("chat_messages/<url>/", views.chat_messages, name="chat_messages"),
]
