import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from django.shortcuts import get_object_or_404
from channels.db import database_sync_to_async
from .models import Chat, Chat_Messages


class ChatMessagesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.url = self.scope['url_route']['kwargs']['url']
        self.chat = await self.get_chat_object()
        
        await self.accept()
        self.chat_messages_task = asyncio.create_task(self.send_chat_messages())


    async def disconnect(self, close_code):
        if hasattr(self, 'chat_messages_task'):
            self.chat_messages_task.cancel()
            try:
                await self.chat_messages_task
            except asyncio.CancelledError:
                pass

    async def send_chat_messages(self):
        last_message_id_sent_to_client = 0
        while True:
            last_message_id_received_from_server, data = await self.fetch_chat_messages(await self.last_message_id_sent_to_client())
            if last_message_id_received_from_server is not None:
                if last_message_id_received_from_server > last_message_id_sent_to_client:
                    last_message_id_sent_to_client = last_message_id_received_from_server

                    await self.send(text_data=json.dumps(data))

                await asyncio.sleep(1)

    @database_sync_to_async
    def fetch_chat_messages(self, last_message_id_sent_to_client):
        chat = Chat.objects.get(url=self.chat.url)
        messages = Chat_Messages.objects.filter(chat=self.chat).order_by("-timestamp")
        messages2 = Chat_Messages.objects.filter(chat=self.chat).order_by("-timestamp")
        
        if messages2.exists():
            last_message2 = messages2.first()
            last_message_id_received_from_server = last_message2.id
        else:
            last_message_id_received_from_server = None

        if last_message_id_sent_to_client is not None:
            messages = messages.filter(id__gt=last_message_id_sent_to_client)

        chat_messages = []
              
        for message in reversed(messages2):
            message_data = {
                "sender": message.sender.username,
                "message": message.message,
                "timestamp": str(message.timestamp),
            }

            chat_messages.append(message_data)
        return last_message_id_received_from_server, {
            "messages": chat_messages,
            "chat_name": chat.chat_name,
        }

    @database_sync_to_async
    def last_message_id_sent_to_client(self):
        messages = Chat_Messages.objects.filter(chat=self.chat).order_by("-timestamp")
        for message in messages:
            return message.id
    
    @database_sync_to_async
    def get_last_message_id(self, chat_messages):
        if chat_messages.exists():
            last_message = chat_messages.first()
            return last_message.id
        return None
    
    @database_sync_to_async
    def get_chat_object(self):
        return get_object_or_404(Chat, url=self.url)