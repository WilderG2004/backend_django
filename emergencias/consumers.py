import json
from channels.generic.websocket import AsyncWebsocketConsumer

class EmergenciaConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        client_ip, client_port = self.scope['client']
        print(f"DEBUG: WebSocket conectado desde IP: {client_ip}:{client_port}")

        # Guarda la IP del cliente conectado para usarla al enviar notificaciones.
        self.client_ip = client_ip

        await self.channel_layer.group_add("emergencias", self.channel_name)
        await self.accept()

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
                "client_send_ts": data["client_send_ts"]
            }))
            print("DEBUG: Servidor recibió 'ping' y respondió con 'pong'.")
            return

        # Procesa otros mensajes del cliente (ej. si el cliente envía una emergencia directamente).
        if data.get("tipo") is not None:
            print(f"DEBUG: Mensaje de emergencia recibido en el servidor desde cliente {self.client_ip}: {data}")
            pass 

    async def enviar_emergencia(self, event):
        # Este método es llamado por la vista (CrearEmergenciaView) vía channel_layer.group_send.
        emergencia_data = event.get("data", {})
        
        # Obtiene la IP del administrador que recibirá esta notificación específica.
        ip_del_administrador_receptor = getattr(self, 'client_ip', 'IP Desconocida')

        # Incluye la IP del administrador receptor en el mensaje para el cliente.
        message_to_client = {
            "type": "nueva_emergencia_notificacion", # Tipo para que el cliente la identifique
            "emergencia": emergencia_data,            # Datos de la emergencia
            "ip_administrador": ip_del_administrador_receptor # IP del administrador que recibe
        }
        
        print(f"DEBUG: Enviando notificación de emergencia a IP {ip_del_administrador_receptor}: {emergencia_data}")
        await self.send(text_data=json.dumps(message_to_client))