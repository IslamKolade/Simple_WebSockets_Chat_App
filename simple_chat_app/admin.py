from django.contrib import admin
from .models import Chat, Chat_Messages
# Register your models here.


class ChatNameSearch(admin.ModelAdmin): 
    search_fields = ('chat_name',)

class ChatMessagesSearch(admin.ModelAdmin): 
    search_fields = ('message',)

admin.site.register(Chat, ChatNameSearch)
admin.site.register(Chat_Messages, ChatMessagesSearch)