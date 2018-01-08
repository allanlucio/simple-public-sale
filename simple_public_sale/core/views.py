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
from core.models import Evento, Prenda, Arrematador, Movimento
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

def manage_event(request,evento_id):
    evento = Evento.objects.get(pk=evento_id)
    prenda = None

    if request.method == 'POST':

        form = MovimentoForm(request.POST)

        if form.is_valid():


            arrematador_nome=form.cleaned_data['nome_arrematador']
            valor=form.cleaned_data['valor_arremate']

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
                    raise ValidationError("Valor do Arremate menor do que o valor inicial da prenda!")

            # data=get_data_stream_view(evento)

            # a=Channel('send-to-group').send({'message': data},immediately=True)

        elif request.method == 'GET':

            prenda = Prenda.objects.get(pk=request.GET.get('prenda'))

        print(prenda)
    else:
        form = MovimentoForm()
    return render(request,'manage_event.html',{'evento':evento,'prenda_selected':'prenda', 'form':form})


def undo_arrematador_lance(request,movimento_id):
    movimento=Movimento.objects.get(pk=movimento_id)
    movimento.delete()
    prenda=movimento.prenda_fk
    evento=prenda.evento_fk
    return redirect(reverse(viewname='manage-event',kwargs={'evento_id':evento.pk})+"?prenda=%s"%prenda.pk)