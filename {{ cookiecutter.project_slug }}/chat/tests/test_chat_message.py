from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from chat.models import Chat


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

    def test_post_message(self):
        chat = Chat.objects.create(
            name='Searching for Baby Yoda',
            admin=self.user,
            description='Too lazy to describe this',
        )

        data = {
            'text': 'Do or do not, there is not try',
            'chat': chat.pk,
        }

        response = self.client.post(
            reverse('chat:list_create_chat_message', kwargs={'uuid': str(chat.uuid)}),
            data=data,
        )
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(reverse('chat:list_create_chat_message', kwargs={'uuid': str(chat.uuid)}))
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertEquals(len(response_data), 1)

        message = response_data[0]
        self.assertEquals(message.get('text'), data.get('text'))

        response = self.client.get(
            reverse('chat:detail_chat_message', kwargs={'uuid': str(chat.uuid), 'pk': message.get('pk')})
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        message = response.json()
        self.assertEquals(message.get('text'), data.get('text'))
