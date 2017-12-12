from django.http import HttpResponse
from channels.handler import AsgiHandler

from django.http import HttpResponse
from channels.handler import AsgiHandler

def http_consumer(message):
    # Make standard HTTP response - access ASGI path attribute directly
    response = HttpResponse("Hello world! You asked for %s" % message.content['path'])
    # Encode that response into message format (ASGI)
    for chunk in AsgiHandler.encode_response(response):
        message.reply_channel.send(chunk)



# In consumers.py
from channels import Group, Channel

def msg_consumer(message):
    # Save to model


    # Broadcast to listening sockets
    Group("chat").send({
        "text": message.content['message'],
    })
# Connected to websocket.connect
def ws_add(message):
    # Accept the incoming connection
    message.reply_channel.send({"accept": True})
    # Add them to the chat group
    Group("chat").add(message.reply_channel)

# Connected to websocket.disconnect
def ws_disconnect(message):
    Group("chat").discard(message.reply_channel)

# Connected to websocket.receive
def ws_message(message):
    # Channel("chat-messages").send({'message': "teste"})
    Group("chat").send({
        "text": "[user] %s" % message.content['text'],
    })