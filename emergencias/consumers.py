import json
from channels.generic.websocket import AsyncWebsocketConsumer
from datetime import datetime

class EmergenciaConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        client_ip, client_port = self.scope['client']
        print(f"DEBUG: WebSocket conectado desde IP: {client_ip}:{client_port}")

        await self.channel_layer.group_add("emergencias", self.channel_name)
        await self.accept()

        # Enviar un mensaje de 'ping' con timestamp al conectarse
        await self.send(text_data=json.dumps({
            "type": "ping",
            "ts": datetime.utcnow().isoformat()  # UTC para evitar desfases
        }))

    async def disconnect(self, close_code):
        client_ip = self.scope['client'][0]
        print(f"DEBUG: WebSocket desconectado desde IP: {client_ip} (Código de cierre: {close_code})")

        await self.channel_layer.group_discard("emergencias", self.channel_name)

    async def receive(self, text_data):
        # Aquí puedes manejar mensajes entrantes si decides usar pings desde el cliente
        data = json.loads(text_data)
        if data.get("type") == "pong":
            print("DEBUG: Cliente respondió al ping (pong recibido)")

    async def enviar_emergencia(self, event):
        data = event.get("data", {})
        await self.send(text_data=json.dumps(data))
