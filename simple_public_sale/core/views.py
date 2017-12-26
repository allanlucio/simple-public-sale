from channels import Channel, Group
from django.shortcuts import render

# Create your views here.
from channels_core.models import GrupoEvento
from core.models import Evento


def send_message(request):
    if request.method == 'POST':

        message=request.POST.get('message')
        a=Channel("chat-messages").send({'message': message},immediately=True)

    return render(request,'simple_chat_send.html')

def list_all_events(request):
    eventos=Evento.objects.all()
    return render(request,'list_all_events.html',{'eventos':eventos})

def watch_event(request,evento_id):

    grupo=GrupoEvento.objects.get(pk=evento_id)
    return render(request,'watch_event.html',{'grupo':grupo})