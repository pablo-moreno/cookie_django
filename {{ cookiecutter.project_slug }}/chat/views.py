from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Chat, ChatMessage
from .permissions import (
    ChatPermission, ChatMessagePermission,
)
from .serializers import ListCreateChatSerializer, ChatDetailSerializer, ChatMessageSerializer


class ListCreateChatView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, ChatPermission, )
    serializer_class = ListCreateChatSerializer

    def get_queryset(self):
        return self.request.user.chats

    def perform_create(self, serializer):
        serializer.save(admin=self.request.user)


class RetrieveUpdateDestroyChatView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, ChatPermission, )
    serializer_class = ChatDetailSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        return self.request.user.chats.all()


class ListCreateChatMessageView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, ChatMessagePermission,)
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        uuid = self.kwargs.get('uuid')
        chat = Chat.objects.get(uuid=uuid)
        return ChatMessage.objects.filter(chat=chat)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RetrieveUpdateDestroyChatMessageView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, ChatMessagePermission,)
    serializer_class = ChatMessageSerializer

    def get_object(self):
        uuid, message_pk = self.kwargs.get('uuid'), self.kwargs.get('pk')
        chat = Chat.objects.get(uuid=uuid)
        return ChatMessage.objects.get(chat=chat, deleted=False, pk=message_pk)


list_create_chat_view = ListCreateChatView.as_view()
retrieve_update_destroy_chat_view = RetrieveUpdateDestroyChatView.as_view()
list_create_chat_message_view = ListCreateChatMessageView.as_view()
retrieve_update_destroy_chat_message_view = RetrieveUpdateDestroyChatMessageView.as_view()
