import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import users_app.routing  # Ensure this is correct
import blog.routing 

django_asgi_app = get_asgi_application()

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mySite.settings')  # Change 'mySite.settings' to your actual settings module if different

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(users_app.routing.websocket_urlpatterns)  # This should be correct
    ),
})




application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(blog.routing.websocket_urlpatterns)
    ),
})
