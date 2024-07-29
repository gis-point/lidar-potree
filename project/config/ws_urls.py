from django.urls import path
from config.consumers import (
    GeneralConsumer,
)

websocket_urlpatterns = [
    path("ws/general/", GeneralConsumer.as_asgi(), name="general"),
]
