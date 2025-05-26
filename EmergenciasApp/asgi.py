import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack # COMENTA ESTA LÍNEA
import emergencias.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EmergenciasApp.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter( # CAMBIA ESTO PARA QUE NO USE AUTHMIDDLEWARESTACK
        emergencias.routing.websocket_urlpatterns
    ),
})