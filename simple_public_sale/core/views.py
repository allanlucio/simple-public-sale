from channels import Channel
from django.core import serializers
from django.core.cache import cache
from django.shortcuts import render
import json
# Create your views here.
from channels_core.models import GrupoEvento
from core.models import Evento, Prenda, Arrematador, Movimento


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
        arrematador_id = request.POST.get('arrematador_id')
        prenda_id = request.POST.get('prenda_id')
        arrematador=Arrematador.objects.filter(pk=arrematador_id)
        prenda = Prenda.objects.get(pk=prenda_id)
        if not arrematador:
            arrematador=Arrematador.objects.create(nome_arrematador=arrematador_nome)
        movimento=Movimento()
        movimento.arrematador_fk=arrematador
        movimento.prenda_fk = prenda
        movimento.valor_arremate=valor
        movimento.save()


        prenda=Prenda.objects.get(pk=prenda_id)
        data={
            'arrematador': arrematador_nome,
            'valor': valor,
            'prenda':serializers.serialize('json', [prenda]),
            'group_id':'%s'%evento.grupo_id
        }

        a=Channel('send-to-group').send({'message': data},immediately=True)




    return render(request,'manage_event.html',{'evento':evento})