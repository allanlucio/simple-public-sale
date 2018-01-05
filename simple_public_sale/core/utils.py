import json

from channels import Channel
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
# from core.models import Movimento
from django.core.cache import cache

from channels_core.custom_serializers import LazyEncoder


def send_to_evento(prenda):
    data = get_data_stream_view(prenda)

    Channel('send-to-group').send({'message': data}, immediately=True)

    return True




def get_data_stream_view(prenda):
    movimentos=prenda.movimento_set.all().order_by('-valor_arremate')
    # movimentos=Movimento.objects.filter(prenda_fk__evento_fk=evento).order_by('-valor_arremate')

    movimento_atual=movimentos.first()
    prenda = movimento_atual.prenda_fk

    movimentos_serialized=serializers.serialize('json',movimentos)
    arrematador_atual_serialized=serializers.serialize('json',[movimento_atual.arrematador_fk])


    prenda_serialized=serializers.serialize('json', [prenda])
    prenda_tipo_serialized=serializers.serialize('json', [prenda.tipo_prenda_fk])
    print(movimentos_serialized)
    print(prenda_serialized)
    print(prenda_tipo_serialized)
    print(arrematador_atual_serialized)
    data = {
        'arrematador_atual': arrematador_atual_serialized,
        'movimentos': movimentos_serialized,
        'prenda': prenda_serialized,
        'prenda_tipo':prenda_tipo_serialized,
        'group_id': '%s' % prenda.evento_fk.grupo_id
    }

    return data

def cache_last_event_message(grupo,message,time=0):
    try:
        message_json=json.loads(message)
    except:
        message_json=json.dumps(message)

    cache.set('last-event-%s' % grupo, json.dumps(message),timeout=None)
    # print(message_json)
    return True