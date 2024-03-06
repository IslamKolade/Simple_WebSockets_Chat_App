from django.db import models
import secrets
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max


class Chat(models.Model):
    url = models.CharField(max_length=255, unique=True, default=None)
    chat_name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name="chatmembers")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.chat_name
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.url = secrets.token_urlsafe(28)
        super().save(*args, **kwargs)
    
    def get_chats(user):
        chats = Chat.objects.filter(members=user).annotate(
            last_message=Max("chat_messages__timestamp")
        ).order_by("-last_message")
        return chats

class Chat_Messages(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="chat_messages")
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Message in Chat: {self.chat.chat_name}"