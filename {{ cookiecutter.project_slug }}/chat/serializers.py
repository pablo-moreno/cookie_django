from rest_framework import serializers

from chat.models import ChatMessage, Chat
from utils.fields import UUIDRelatedField


class ChatMessageSerializer(serializers.ModelSerializer):
    chat = UUIDRelatedField(queryset=Chat.objects.all())

    class Meta:
        model = ChatMessage
        fields = (
            'text',
            'user',
            'chat',
            'date',
        )
        read_only_fields = (
            'user',
            'date',
        )
