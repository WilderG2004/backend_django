import json
from channels.generic.websocket import AsyncWebsocketConsumer

class EmergenciaConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("emergencias", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("emergencias", self.channel_name)

    async def receive(self, text_data):
        # Aquí normalmente no recibimos nada, solo enviamos.
        pass

    async def enviar_emergencia(self, event):
        await self.send(text_data=json.dumps(event['data']))
