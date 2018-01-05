from channels import Channel
from decimal import Decimal
from django.core import serializers
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.shortcuts import render
import json
# Create your views here.
from channels_core.models import GrupoEvento
from core.models import Evento, Prenda, Arrematador, Movimento
from core.utils import get_data_stream_view, send_to_evento


def send_message(request):
    if request.method == 'POST':

        message=request.POST.get('message')

        a=Channel("chat-messages").send({'message': message},immediately=True)

    return render(request,'simple_chat_send.html')

def list_all_events(request):
    eventos=Evento.objects.all()
    return render(request,'list_all_events.html',{'eventos':eventos})

def watch_event(request,group_id):

    grupo=GrupoEvento.objects.get(pk=group_id)
    return render(request,'watch_event.html',{'grupo':grupo})

def manage_event(request,evento_id):
    evento = Evento.objects.get(pk=evento_id)
    if request.method == 'POST':

        arrematador_nome=request.POST.get('arrematador')
        valor=request.POST.get('valor')

        prenda_id = request.POST.get('prenda_id')

        prenda = Prenda.objects.get(pk=prenda_id, evento_fk=evento)

        arrematador=Arrematador.objects.get_or_create(nome_arrematador=arrematador_nome)[0]

        movimento=Movimento(arrematador_fk=arrematador,prenda_fk=prenda,valor_arremate=valor)


        movimento_anterior = Movimento.objects.filter(prenda_fk = prenda_id)

        if movimento_anterior:
            movimento_anterior=movimento_anterior[0]

            if Decimal(movimento.valor_arremate) <= movimento_anterior.valor_arremate:
                raise ValidationError("Valor do Arremate menor do que o valor atual!")
            else:

                movimento.save()
                # send_to_evento(evento=evento)
        else:
            if Decimal(movimento.valor_arremate) <= prenda.valor_inicial:
                raise ValidationError("Valor do Arremate menor do que o valor atual!")

        # data=get_data_stream_view(evento)

        # a=Channel('send-to-group').send({'message': data},immediately=True)




    return render(request,'manage_event.html',{'evento':evento})