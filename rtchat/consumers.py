from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import GroupMessage
import json
from django.contrib.auth.models import User

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = 'Group1'
        async_to_sync(self.channel_layer.group_add) (
            self.group_name,
            self.channel_name,
        )
        self.accept()
    
    def receive(self, text_data):
        text_data_dict = json.loads(text_data)
        message = text_data_dict['message']
        username = text_data_dict['username']
        self.user = User.objects.get(username=username)

        GroupMessage.objects.create(
            text = message,
            author = self.user,
        )

        async_to_sync(self.channel_layer.group_send) (
            self.group_name,
            {
                'type': 'chat',
                'message': message,
                'username': username,
            }
        )

    def chat(self, event):
        message = event['message']
        username = event['username']

        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message,
            'username': username,
        }))
