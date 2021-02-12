from channels.db import database_sync_to_async

from chat.serializers import ChatMessageSerializer
from utils.channels.consumers import AsyncJsonWebsocketConsumerWithPerms


class ChatConsumer(AsyncJsonWebsocketConsumerWithPerms):
    permission_classes = ()
    serializer_class = ChatMessageSerializer

    def __init__(self, *args, **kwargs):
        self.user = None
        self.groups = set()
        super().__init__(*args, **kwargs)

    async def connect(self):
        self.user = self.scope.get('user')
        self.groups = await self.get_user_channels()
        await self.connect_to_channels()
        await super().connect()

    @database_sync_to_async
    def save_message(self, message):
        serializer = self.serializer_class(data=message)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['user'] = self.user
        serializer.save()

        return message, message['chat']

    async def receive_json(self, content, **kwargs):
        message, chat_id = await self.save_message(content)

        await self.channel_layer.group_send(
            f'chat_{chat_id}',
            {
                "type": "chat.message",
                "content": message,
            },
        )

    async def chat_message(self, event):
        await self.send_json(
            event['content'],
        )
