
from django.http import HttpResponse
from channels.handler import AsgiHandler
import json
from channels import Group
from channels.sessions import channel_session
from urllib.parse import parse_qs
from django.core.cache import cache
# Connected to websocket.connect
from channels_core.models import GrupoEvento
from core.utils import cache_last_event_message


def connect_group_safe(message,username,group_id):

    grupo_evento = GrupoEvento.objects.get(pk=group_id)
    if (grupo_evento.evento.is_online()):
        # Group(group_id).discard(message.reply_channel)
        Group(group_id).add(message.reply_channel)
        print([a for a in Group(group_id).channel_layer.group_channels(group_id)])
        data = cache.get('last-event-%s' % group_id)
        message.reply_channel.send({"text": data})
        return True
    else:
        message.reply_channel.send({"text": "Evento offline"})
        message.reply_channel.send({"close": True})
        return False

@channel_session
def ws_connect(message, room_name):
    # Accept connection

    message.reply_channel.send({"accept": True})
    
    # Parse the query string
    params = parse_qs(message.content["query_string"])
    #Params receives a GET query with url.com/?username=yourUserName
    print(params)
    if b"username" in params and b"group_id" in params:
        # Set the username in the session
        message.channel_session["username"] = params[b"username"][0].decode("utf8")
        group_id=params[b"group_id"][0].decode("utf8")
        connect_group_safe(message,username=message.channel_session["username"],group_id=group_id)
    else:
        # Close the connection.
        message.reply_channel.send({"close": True})

# Connected to websocket.receive
@channel_session
def ws_message(message, room_name):
    data=json.loads(message.content.get('text'))
    group_id=data.get('group_id')
    username=data.get('username')
    ativo=connect_group_safe(message, username=username,group_id=group_id)
    if ativo:
        print("KeepAlive")

# Connected to websocket.disconnect
@channel_session
def ws_disconnect(message, room_name):
    Group("chat").discard(message.reply_channel)

#

def msg_consumer(message):
    # Save to model

    message=message.content.get('message')
    grupo=message.get('group_id')
    cache_last_event_message(grupo=grupo,message=message)
    message_json=json.dumps(message)
    # cache.set('last-event-%s'%grupo,message_json)
    print('enviando para: %s' % grupo)

    g=Group(grupo).send({
        "text": message_json,
    },immediately=True)
    print(g)
# # Connected to websocket.connect
# def ws_add(message):
#     # Accept the incoming connection
#     message.reply_channel.send({"accept": True})
#     # Add them to the chat group
#     Group("chat").add(message.reply_channel)
#
# # Connected to websocket.disconnect
# def ws_disconnect(message):
#     Group("chat").discard(message.reply_channel)
#
# # Connected to websocket.receive
# def ws_message(message):
#     # Channel("chat-messages").send({'message': "teste"})
#     Group("chat").send({
#         "text": "[user] %s" % message.content['text'],
#     })