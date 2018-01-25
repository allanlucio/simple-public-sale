from channels import Channel
from decimal import Decimal
from django.core import serializers
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
import json
# Create your views here.
from django.urls import reverse
from django.views.decorators.http import require_POST

from channels_core.models import GrupoEvento
from core.decorators import exceptions_to_messages
from core.models import Evento, Prenda, Participante, Movimento
from core.utils import get_data_stream_view, send_to_evento

from .forms import MovimentoForm


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

def list_gift_finishers(request,evento_id):
    evento = Evento.objects.get(pk=evento_id)
    prendas= evento.prenda_set.all()

    return render(request,'list_gift_finishers.html',{'evento':evento,'prendas':prendas})

@exceptions_to_messages
def manage_event(request,evento_id):
    evento = Evento.objects.get(pk=evento_id)
    prenda = None

    if request.method == 'POST' and 'btn-enviar' in request.POST:

        form = MovimentoForm(request.POST, data = [request.POST.get('prenda_id')])

        if form.is_valid():


            arrematador_nome=request.POST.get('nome_arrematador')
            valor=request.POST.get('valor_arremate')

            prenda_id = request.POST.get('prenda_id')

            prenda = Prenda.objects.get(pk=prenda_id, evento=evento)

            arrematador=Participante.objects.get_or_create(apelido=arrematador_nome.upper())[0]

            movimento=Movimento(arrematador=arrematador,prenda=prenda,valor=valor)



            movimento_anterior = Movimento.objects.filter(prenda__pk = prenda_id).order_by('-valor')


            movimento.save()

            # data=get_data_stream_view(evento)

            # a=Channel('send-to-group').send({'message': data},immediately=True)

        elif request.method == 'GET':

            prenda = Prenda.objects.get(pk=request.GET.get('prenda'))

        print(prenda)

    else:
        form = MovimentoForm()
    return render(request,'manage_event.html',{'evento':evento,'prenda_selected':prenda, 'form':form})
@exceptions_to_messages
def arrematar_prenda(request, prenda_id, evento_id):

        prenda = Prenda.objects.get(pk=prenda_id, evento=evento_id)

        if prenda.arrematada == False:
            prenda.arrematada = True
            prenda.save()
            print("Arrematou!")

        return redirect(reverse(viewname='manage-event', kwargs={'evento_id': evento_id}) + "?prenda=%s" % prenda_id)

@exceptions_to_messages
def undo_arrematar_prenda(request, prenda_id, evento_id):
    prenda = Prenda.objects.get(pk=prenda_id, evento=evento_id)

    if prenda.arrematada == True:
        prenda.arrematada = False
        prenda.save()
        print("Retirada do arremate da prenda")

    return redirect(reverse(viewname='manage-event', kwargs={'evento_id': evento_id}) + "?prenda=%s" % prenda_id)

@exceptions_to_messages
def undo_donation(request, prenda_id, evento_id):
    prenda = Prenda.objects.get(parent=prenda_id, evento=evento_id)
    parent = prenda.parent
    prenda.delete()


    return redirect(reverse(viewname='manage-event', kwargs={'evento_id': evento_id}) + "?prenda=%s" % parent.pk)

@exceptions_to_messages
def undo_arrematador_lance(request,movimento_id):
    movimento=Movimento.objects.get(pk=movimento_id)
    movimento.delete()
    prenda=movimento.prenda
    evento=prenda.evento
    return redirect(reverse(viewname='manage-event',kwargs={'evento_id':evento.pk})+"?prenda=%s"%prenda.pk)


@exceptions_to_messages
def donate_prenda(request,prenda_id):
    prenda=Prenda.objects.get(pk=prenda_id)

    prenda.get_prenda_clone()
    evento = prenda.evento
    print('oi')

    return redirect(reverse(viewname='manage-event', kwargs={'evento_id': evento.pk}) + "?prenda=%s" % prenda.pk)