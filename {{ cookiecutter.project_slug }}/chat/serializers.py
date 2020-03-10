from django.contrib.auth.models import User
from rest_framework.serializers import (
    ModelSerializer, SerializerMethodField, DateTimeField
)

from .models import Chat, ChatMessage


class ChatMemberSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk', 'username', 'email',
            'first_name', 'last_name',
        )


class ChatAdminSerializer(ChatMemberSerializer):
    class Meta(ChatMemberSerializer.Meta):
        pass


class ListCreateChatSerializer(ModelSerializer):
    admin = ChatMemberSerializer(read_only=True)
    members = SerializerMethodField(read_only=True)

    def get_members(self, chat):
        return ChatMemberSerializer(chat.members.all(), many=True).data

    class Meta:
        model = Chat
        fields = (
            'pk', 'uuid', 'name', 'admin',
            'description', 'members',
        )


class ChatDetailSerializer(ListCreateChatSerializer):
    pass


class ChatMessageSerializer(ModelSerializer):
    user = ChatMemberSerializer(read_only=True)
    creation_date = DateTimeField(read_only=True)

    class Meta:
        model = ChatMessage
        fields = (
            'pk', 'text', 'user',
            'chat', 'creation_date',
        )
