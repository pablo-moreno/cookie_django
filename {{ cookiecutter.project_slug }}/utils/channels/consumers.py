from channels.db import database_sync_to_async
from channels.generic.websocket import (
    WebsocketConsumer, AsyncWebsocketConsumer, JsonWebsocketConsumer, AsyncJsonWebsocketConsumer,
)
from chat.models import ChatMember, Chat
from .mixins import AsyncWebsocketPermissionMixin, WebsocketPermissionMixin


class CustomWebsocketMixin(object):
    """
        Mixin that adds the user to the WebsocketConsumer
    """
    @database_sync_to_async
    def get_user_channels(self):
        """
            Connects a user's reply-channels to all the chats the user is
            member of. This is done in lazy mode.
        """
        user_groups = set()

        chat_ids = ChatMember.objects.select_related('chat')\
            .filter(user=self.user)\
            .values_list('chat__uuid', flat=True)

        for chat_id in chat_ids:
            channel_name = f'chat_{chat_id}'
            user_groups.add(channel_name)

        return user_groups

    async def connect_to_channels(self):
        """
            This actually connects the user to the channels
        """
        for group in self.groups:
            await self.channel_layer.group_add(group, self.channel_name)

    def disconnect_user_channels_from_chat(self, chat: Chat):
        discarded_groups = [channel for channel in self.groups if str(chat.pk) in channel]

        for group in discarded_groups:
            self.channel_layer.group_discard(group, self.channel_name)

        self.groups = self.groups - discarded_groups

    def disconnect_channel_from_chats(self):
        for group in self.groups:
            self.channel_layer.group_discard(group, self.channel_name)


class AsyncWebsocketConsumerWithPerms(CustomWebsocketMixin, AsyncWebsocketConsumer, WebsocketPermissionMixin):
    """
        Asynchronous Websocket Consumer with permissions
    """
    pass


class AsyncJsonWebsocketConsumerWithPerms(CustomWebsocketMixin, AsyncJsonWebsocketConsumer, AsyncWebsocketPermissionMixin):
    """
        Asynchronous Websocket Consumer with permissions that handles sending and receiving json payloads
    """
    pass


class WebsocketConsumerWithPerms(WebsocketConsumer, WebsocketPermissionMixin, CustomWebsocketMixin):
    """
        Synchronous Websocket Consumer with permissions
    """
    pass


class JsonWebsocketConsumerWithPerms(JsonWebsocketConsumer, WebsocketPermissionMixin, CustomWebsocketMixin):
    """
        Synchronous Websocket Consumer with permissions that handles sending and receiving json payloads
    """
    pass
