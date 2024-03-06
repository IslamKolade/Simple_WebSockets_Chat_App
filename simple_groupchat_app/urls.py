from django.urls import path
from . import views

urlpatterns = [
    path("join_group_chat/", views.join_group_chat, name="join_group_chat"),
    path("create_group_chat/", views.create_group_chat, name="create_group_chat"),
    path("group_messages/<url>/", views.group_messages, name="group_messages"),
]
