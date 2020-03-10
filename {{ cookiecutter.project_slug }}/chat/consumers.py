import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.models import ChatMessage, Chat
from .mixins import PermissionMixin
from .ws_permissions import Any


class ChatConsumer(AsyncWebsocketConsumer, PermissionMixin):
    permission_classes = (Any, )

    def __init__(self, *args, **kwargs):
        self.user = None
        self.chats = set()

        super().__init__(*args, **kwargs)

    async def connect(self):
        self.user = self.scope['user']
        self.chats = await self.get_user_chats()

        for chat in self.chats:
            await self.channel_layer.group_add(
                chat,
                self.channel_name,
            )

        await self.accept()

    async def disconnect(self, close_code):
        for chat in self.chats:
            await self.channel_layer.group_discard(chat, self.channel_name)

    async def receive(self, text_data=None, *args, **kwargs):
        """
        Event listening for receiving messages.

        Expects text_data to be like:
            text_data = {
                'text': 'message text',
                'chat': 'chat.uuid'
            }
        """
        message = json.loads(text_data)
        message = await self.save_message(message)

        await self.channel_layer.group_send(message.chat.uuid, message.text)

    @database_sync_to_async
    def get_user_chats(self):
        return set(self.user.chats.values_list('uuid', flat=True))

    @database_sync_to_async
    def save_message(self, message):
        chat = Chat.objects.get(uuid=message.get('uuid'))

        return ChatMessage.objects.create(
            text=message.get('text'),
            user=self.user,
            chat=chat,
        )
