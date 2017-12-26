from channels import Channel
from django.core import serializers

from django.shortcuts import render

# Create your views here.
from channels_core.models import GrupoEvento
from core.models import Evento, Prenda


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

        arrematador=request.POST.get('arrematador')
        valor=request.POST.get('valor')
        prenda_id = request.POST.get('prenda_id')
        prenda=Prenda.objects.get(pk=prenda_id)
        data={
            'arrematador': arrematador,
            'valor': valor,
            'prenda':serializers.serialize('json', [prenda]),
            'group_id':'%s'%evento.grupo_id
        }

        a=Channel('chat-messages').send({'message': data},immediately=True)

    return render(request,'manage_event.html',{'evento':evento})