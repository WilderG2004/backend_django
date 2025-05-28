import json
from channels.generic.websocket import AsyncWebsocketConsumer

class EmergenciaConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        client_ip, client_port = self.scope['client']
        print(f"DEBUG: WebSocket conectado desde IP: {client_ip}:{client_port}")

        await self.channel_layer.group_add("emergencias", self.channel_name)
        await self.accept()

        # El servidor ya no envía 'ping' al conectar. La medición RTT es iniciada por el cliente.

    async def disconnect(self, close_code):
        client_ip = self.scope['client'][0]
        print(f"DEBUG: WebSocket desconectado desde IP: {client_ip} (Código de cierre: {close_code})")
        await self.channel_layer.group_discard("emergencias", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        
        # Responde a los 'ping' del cliente para el cálculo de RTT.
        if data.get("type") == "ping" and data.get("client_send_ts"):
            await self.send(text_data=json.dumps({
                "type": "pong",
                "client_send_ts": data["client_send_ts"] # Devuelve el timestamp original del cliente
            }))
            print("DEBUG: Servidor recibió 'ping' y respondió con 'pong'.")
            return

        # Procesa otros mensajes, como las emergencias.
        if data.get("tipo") is not None:
            print(f"DEBUG: Mensaje de emergencia recibido en el servidor: {data}")
            pass # Aquí iría tu lógica para manejar la emergencia

    async def enviar_emergencia(self, event):
        # Envía mensajes de emergencia a los clientes conectados.
        data = event.get("data", {})
        print(f"DEBUG: Enviando emergencia desde el servidor a cliente: {data}")
        await self.send(text_data=json.dumps(data))