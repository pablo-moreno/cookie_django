from django.utils import timezone
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User
from config.models import Deletable


class Chat(models.Model):
    uuid = models.UUIDField(default=uuid4, db_index=True)
    members = models.ManyToManyField(User, related_name='chats')
    name = models.CharField(max_length=60, blank=False, null=False)
    description = models.CharField(max_length=140, default='', blank=True, null=True)
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    creation_date = models.DateTimeField(default=timezone.now)


class ChatMessage(Deletable):
    text = models.CharField(max_length=500, blank=False, null=False, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE, null=False)
    creation_date = models.DateTimeField(default=timezone.now)
