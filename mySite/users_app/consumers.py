# users_app/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from .models import Message
from channels.db import database_sync_to_async

User = get_user_model()

class MessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sender = self.scope["user"]
        self.recipient_username = self.scope['url_route']['kwargs']['username']
        self.recipient = await database_sync_to_async(User.objects.get)(username=self.recipient_username)

        # Unique group name for each conversation
        self.room_name = f"chat_{min(self.sender.username, self.recipient.username)}_{max(self.sender.username, self.recipient.username)}"
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_text = data['message']

        # Save the message to the DB
        await self.save_message(self.sender, self.recipient, message_text)

        # Broadcast to room
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat_message',
                'message': message_text,
                'sender': self.sender.username
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender']
        }))

    @database_sync_to_async
    def save_message(self, sender, recipient, text):
        return Message.objects.create(sender=sender, recipient=recipient, text=text)
