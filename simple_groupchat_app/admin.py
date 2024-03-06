from django.contrib import admin
from .models import Group_Chat, Group_Messages
# Register your models here.


class GroupNameSearch(admin.ModelAdmin): 
    search_fields = ('group_name',)

class GroupMessagesSearch(admin.ModelAdmin): 
    search_fields = ('message',)

admin.site.register(Group_Chat, GroupNameSearch)
admin.site.register(Group_Messages, GroupMessagesSearch)