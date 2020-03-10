from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from chat.models import Chat
from chat.serializers import ListCreateChatSerializer, ChatMemberSerializer


class TestCreateChat(APITestCase):
    def setUp(self):
        self.username = 'yoda'
        self.password = 'ImNotBabyYoda'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
            email=f'{self.username}@starwars.com',
        )
        self.client.force_login(self.user)

    def test_chat_member_serializer(self):
        serializer = ChatMemberSerializer(self.user)
        data = serializer.data
        self.assertEqual(data.get('username'), self.username)
        self.assertEqual(data.get('email'), self.user.email)

    def test_chat_serializer(self):
        data = {'name': 'Searching for Baby Yoda'}
        serializer = ListCreateChatSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        chat = serializer.save(admin=self.user)
        self.assertEquals(chat.admin.pk, self.user.pk)
        self.assertIn(self.user, chat.members.all())

        serialized_chat = ListCreateChatSerializer(chat).data
        self.assertEqual(serialized_chat.get('admin').get('username'), self.username)
        self.assertEqual(len(serialized_chat.get('members')), 1)

    def test_create_chat(self):
        data = {'name': 'Searching for Baby Yoda'}
        response = self.client.post(reverse('chats:list_create_chat'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = response.json()
        self.assertEqual(response_data.get('name'), data.get('name'))

    def test_retrieve_chat(self):
        data = {'name': 'Searching for Baby Yoda'}
        response = self.client.post(reverse('chats:list_create_chat'), data=data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        response_data = response.json()
        response = self.client.get(reverse('chats:detail_chat', kwargs={'uuid': response_data.get('uuid')}))
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertEquals(response_data.get('name'), data.get('name'))
