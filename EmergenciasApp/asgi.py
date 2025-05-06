import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import emergencias.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EmergenciasApp.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            emergencias.routing.websocket_urlpatterns
        )
    ),
})
