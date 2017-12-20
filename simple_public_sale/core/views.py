from channels import Channel, Group
from django.shortcuts import render

# Create your views here.

def send_message(request):
    if request.method == 'POST':

        message=request.POST.get('message')


        a=Channel("chat-messages").send({'message': message},immediately=True)
        print(Group('chat').get_channels())
    return render(request,'simple_chat_send.html')