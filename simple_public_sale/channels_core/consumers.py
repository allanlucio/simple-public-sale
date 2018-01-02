from django.http import HttpResponse
from channels.handler import AsgiHandler
import json
from channels import Group
from channels.sessions import channel_session
from urllib.parse import parse_qs

# Connected to websocket.connect
from channels_core.models import GrupoEvento


@channel_session
def ws_connect(message, room_name):
    # Accept connection

    message.reply_channel.send({"accept": True})
    
    # Parse the query string
    params = parse_qs(message.content["query_string"])
    #Params receives a GET query with url.com/?username=yourUserName
    if b"username" in params and b"group_id" in params:
        # Set the username in the session
        message.channel_session["username"] = params[b"username"][0].decode("utf8")
        group_id=params[b"group_id"][0].decode("utf8")
        grupo_evento=GrupoEvento.objects.get(pk=group_id)
        if(grupo_evento.online):
            Group(group_id).add(message.reply_channel)
            message.reply_channel.send({"text":"Conectado"})
        else:
            message.reply_channel.send({"text":"Evento offline"})
            message.reply_channel.send({"close": True})



    else:
        # Close the connection.
        message.reply_channel.send({"close": True})

# Connected to websocket.receive
@channel_session
def ws_message(message, room_name):
    Group("chat").send({
        "text": json.dumps({
            "text": message["text"],
            "username": message.channel_session["username"],
        }),
    })

# Connected to websocket.disconnect
@channel_session
def ws_disconnect(message, room_name):
    Group("chat").discard(message.reply_channel)
# from django.http import HttpResponse
# from channels.handler import AsgiHandler
#
# def http_consumer(message):
#     # Make standard HTTP response - access ASGI path attribute directly
#     response = HttpResponse("Hello world! You asked for %s" % message.content['path'])
#     # Encode that response into message format (ASGI)
#     for chunk in AsgiHandler.encode_response(response):
#         message.reply_channel.send(chunk)
#
#
#
# # In consumers.py
# from channels import Group, Channel
#
def msg_consumer(message):
    # Save to model

    print(message.content.get('message'))
    # Broadcast to listening sockets
    Group("chat").send({
        "text": message.content['message'],
    })
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