import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from django.shortcuts import get_object_or_404
from channels.db import database_sync_to_async
from .models import Group_Chat, Group_Messages


class GroupChatMessagesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.url = self.scope['url_route']['kwargs']['url']
        self.group_chat = await self.get_group_chat_object()
        
        await self.accept()
        self.group_chat_messages_task = asyncio.create_task(self.send_group_chat_messages())


    async def disconnect(self, close_code):
        if hasattr(self, 'group_chat_messages_task'):
            self.group_chat_messages_task.cancel()
            try:
                await self.group_chat_messages_task
            except asyncio.CancelledError:
                pass

    async def send_group_chat_messages(self):
        last_message_id_sent_to_client = 0
        while True:
            last_message_id_received_from_server, data = await self.fetch_group_chat_messages(await self.last_message_id_sent_to_client())
            if last_message_id_received_from_server is not None:
                if last_message_id_received_from_server > last_message_id_sent_to_client:
                    last_message_id_sent_to_client = last_message_id_received_from_server

                    await self.send(text_data=json.dumps(data))

                await asyncio.sleep(1)

    @database_sync_to_async
    def fetch_group_chat_messages(self, last_message_id_sent_to_client):
        group = Group_Chat.objects.get(url=self.group_chat.url)
        messages = Group_Messages.objects.filter(group=self.group_chat).order_by("-timestamp")
        messages2 = Group_Messages.objects.filter(group=self.group_chat).order_by("-timestamp")
        
        if messages2.exists():
            last_message2 = messages2.first()
            last_message_id_received_from_server = last_message2.id
        else:
            last_message_id_received_from_server = None

        if last_message_id_sent_to_client is not None:
            messages = messages.filter(id__gt=last_message_id_sent_to_client)

        group_messages = []
              
        for message in reversed(messages2):
            message_data = {
                "sender": message.sender.username,
                "message": message.message,
                "timestamp": str(message.timestamp),
            }

            group_messages.append(message_data)
            
        return last_message_id_received_from_server, {
            "messages": group_messages
        }

    @database_sync_to_async
    def last_message_id_sent_to_client(self):
        messages = Group_Messages.objects.filter(group=self.group_chat).order_by("-timestamp")
        for message in messages:
            return message.id
    
    @database_sync_to_async
    def get_last_message_id(self, group_chat_messages):
        if group_chat_messages.exists():
            last_message = group_chat_messages.first()
            return last_message.id
        return None
    
    @database_sync_to_async
    def get_group_chat_object(self):
        return get_object_or_404(Group_Chat, url=self.url)