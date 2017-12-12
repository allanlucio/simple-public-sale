from channels import Channel
from django.shortcuts import render

# Create your views here.

def send_message(request):
    if request.method == 'POST':

        message=request.POST.get('message')
        print(message)
        a=Channel("chat-messages").send({'message': message})
        print(a)
    return render(request,'simple_chat_send.html')