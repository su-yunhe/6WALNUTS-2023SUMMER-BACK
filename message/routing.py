
from django.urls import path

import file_manage
import message
from message import consumers
from message.consumers import ChatConsumer, FileConsumer

websocket_urlpatterns = [
    path('ws/message/', ChatConsumer.as_asgi()),
    path('ws/file/', FileConsumer.as_asgi()),
]
