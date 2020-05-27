from django.urls import path

from channels.routing import ProtocolTypeRouter, URLRouter

from rooms.consumers import RoomConsumer

application = ProtocolTypeRouter({
    'websocket': URLRouter([
        path(r'ws/rooms/<str:room_id>', RoomConsumer),
    ])
})