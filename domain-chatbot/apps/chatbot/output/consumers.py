import json
import logging
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

chat_channel = "chat_channel"
logger = logging.getLogger(__name__)


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()
        # 将连接的客户端添加到特定频道
        async_to_sync(self.channel_layer.group_add)(
            chat_channel,  # 设置频道名称
            self.channel_name
        )
        logger.info(f'=> ws connect group : {chat_channel}')

    def disconnect(self, close_code):
        # 在客户端断开连接时从频道中移除
        async_to_sync(self.channel_layer.group_discard)(
            chat_channel,  # 设置频道名称
            self.channel_name
        )

    def receive(self, text_data):
        logger.info(f"=> run receive:{text_data}")
        # self.send(text_data=json.dumps({"message": text_data}))

      # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        logger.info(f"=> run chat_message :{message}")
        text_data = json.dumps({"message": message})
        self.send(text_data=text_data)
