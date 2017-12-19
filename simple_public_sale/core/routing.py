from channels.routing import route
from .consumers import *
channel_routing = [
    route("websocket.connect", ws_connect, path=r"^/(?P<room_name>[a-zA-Z0-9_]+)/$"),
    route("websocket.receive", ws_message , path=r"^/(?P<room_name>[a-zA-Z0-9_]+)/$"),
    route("websocket.disconnect", ws_disconnect , path=r"^/(?P<room_name>[a-zA-Z0-9_]+)/$"),
    # route("chat-messages", msg_consumer),
]