from channels.routing import route
from .consumers import *
channel_routing = [
    route("websocket.connect", ws_add, path='/chat/'),
    route("websocket.receive", ws_message , path='/chat/'),
    route("websocket.disconnect", ws_disconnect , path='/chat/'),
    route("chat-messages", msg_consumer),
]