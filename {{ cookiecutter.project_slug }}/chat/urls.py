from django.urls import path
from .views import (
    list_create_chat_view, retrieve_update_destroy_chat_view,
    list_create_chat_message_view, retrieve_update_destroy_chat_message_view,
)

app_name = 'chat'

urlpatterns = [
    path('', list_create_chat_view, name='list_create_chat'),
    path('<uuid>', retrieve_update_destroy_chat_view, name='detail_chat'),
    path('<uuid>/messages', list_create_chat_message_view, name='list_create_chat_message'),
    path('<uuid>/messages/<pk>', retrieve_update_destroy_chat_message_view, name='detail_chat_message'),
]
