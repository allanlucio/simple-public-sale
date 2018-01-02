import json

from channels import Channel
from django.core import serializers

from core.models import Movimento
from django.core.cache import cache

def send_to_evento(evento):
    data = get_data_stream_view(evento)

    Channel('send-to-group').send({'message': data}, immediately=True)

    return True

def get_data_stream_view(evento):
    movimentos=Movimento.objects.filter(prenda_fk__evento_fk=evento).order_by('-valor_arremate')

    movimento_atual=movimentos[0]
    prenda = movimento_atual.prenda_fk

    movimentos_serialized=serializers.serialize('json',movimentos)
    arrematador_atual_serialized=serializers.serialize('json',[movimento_atual.arrematador_fk])

    print(movimentos_serialized)
    prenda_serialized=serializers.serialize('json', [prenda])
    data = {
        'arrematador_atual': arrematador_atual_serialized,
        'movimentos': movimentos_serialized,
        'prenda': prenda_serialized,
        'group_id': '%s' % evento.grupo_id
    }

    return data

def cache_last_event_message(grupo,message,time=0):
    try:
        message_json=json.loads(message)
    except:
        message_json=json.dumps(message)

    cache.set('last-event-%s' % grupo, json.dumps(message))

    return True