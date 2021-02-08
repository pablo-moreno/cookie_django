from django.db import models
from django.contrib.auth import get_user_model
from uuid import uuid4


User = get_user_model()


class Chat(models.Model):
    uuid = models.UUIDField(default=uuid4)


class ChatMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='members')


class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    text = models.CharField(max_length=1000)
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
