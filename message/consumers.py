import json
from asgiref.sync import async_to_sync
from channels.exceptions import StopConsumer
from channels.generic.websocket import WebsocketConsumer
from message.models import Message, UserMessage
from station_manage.models import Files

user_list = []


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print('begin connect')
        self.room_group_name = (self.scope['query_string'].decode("utf-8"))[3:]
        print(self.room_group_name)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, message):
        print('disconnect:')
        print(self.channel_name, self.room_group_name)
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)
        raise StopConsumer()

    def websocket_receive(self, message):
        # 通知组内的所有客户端，执行 xx_oo 方法，在此方法中自己可以去定义任意的功能。
        print('begin group_send')
        data = json.loads(message['text'])
        print(data)
        is_remind = data.get('mention')  # is_remind为true，则表示携带@信息，需要进一步处理
        chatid = data.get('chatId')
        username = data.get('senderName')
        content = data.get('content')

        new_message = Message()
        new_message.chatId_id = chatid
        new_message.senderName = username
        new_message.content = content
        new_message.save()
        # time = new_message.time
        if is_remind:  # 处理@人的情况
            mentionlist = data.get('mentionlist')
            for obj in mentionlist:
                new_usermessage = UserMessage()
                new_usermessage.messageId_id = new_message.messageId
                new_usermessage.targetId_id = obj
                new_usermessage.save()
        data['messageId'] = new_message.messageId
        time = new_message.time
        data['time'] = time.strftime('%Y-%m-%d %H:%M:%S')
        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {'type': "chat_message", 'data': data})

    def chat_message(self, event):
        text = json.dumps(event['data'])
        print(text)
        self.send(text)


class FileConsumer(WebsocketConsumer):
    def connect(self):
        print('begin connect')
        self.room_group_name = (self.scope['query_string'].decode("utf-8"))[3:]
        print(self.room_group_name)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, message):
        print('disconnect:')
        print(self.channel_name, self.room_group_name)
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)
        raise StopConsumer()

    def websocket_receive(self, message):
        # 通知组内的所有客户端，执行 xx_oo 方法，在此方法中自己可以去定义任意的功能。
        print('begin group_send')
        data = json.loads(message['text'])
        print(data)
        fileid = data.get('fileId')
        content = data.get('fileInclude')
        file = Files.objects.get(fileId=fileid)
        file.fileInclude = content
        file.save()
        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {'type': "file_message", 'data': data})

    def file_message(self, event):
        text = json.dumps(event['data'])
        print(text)
        self.send(text)
