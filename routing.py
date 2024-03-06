from django.urls import path
from simple_chat_app.consumers import ChatMessagesConsumer
from simple_groupchat_app.consumers import GroupChatMessagesConsumer

websocket_urlpatterns = [
    path("ws/chat_messages/<url>/", ChatMessagesConsumer.as_asgi()),
    path("ws/group_chat_messages/<url>/", GroupChatMessagesConsumer.as_asgi())
]


