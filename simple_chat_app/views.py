from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Chat, Chat_Messages
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib import messages

@login_required
def join_chat(request):
    chat_name = request.GET.get("chat_name")
    
    if chat_name:
        try:
            chat = Chat.objects.get(chat_name=chat_name)
            
            if chat.members.count() >= 2: 
                messages.error(request, "This chat is already at its maximum capacity.")
                return render(request, 'join_chat.html')
            
            if request.user not in chat.members.all():
                chat.members.add(request.user)
                messages.success(request, "Welcome to " + chat.chat_name + "!")
                return redirect('chat_messages', url=chat.url)
            else:
                messages.warning(request, "You're already a member of this chat.")
                return redirect('chat_messages', url=chat.url)
        except Chat.DoesNotExist:
            messages.error(request, "Invalid chat name.")
            return render(request, 'join_chat.html')
    else:
        return render(request, 'join_chat.html')


@login_required
def create_chat(request):
    if request.method == 'POST':
        chat_name = request.POST.get('chat_name')
        if chat_name.strip() == '':
            return HttpResponseForbidden()
        stripped_chat_name = chat_name.strip()
        new_chat = Chat.objects.create(chat_name=stripped_chat_name)
        new_chat.members.add(request.user)
        return redirect('chat_messages', url=new_chat.url)
    return render(request, 'create_chat.html')


@login_required
def chat_messages(request, url):
    chat = Chat.objects.get(url=url)
    if request.user not in chat.members.all():
        return HttpResponseForbidden()
    
    if request.method == "POST":
        message_sent = request.POST.get("message")
        
        message = Chat_Messages.objects.create(
            chat=chat,
            sender=request.user,
            message=message_sent,
        )
        
        message.save()
        
        allmessages = 'messages'
        data = {
            'messages': allmessages
        }
        return JsonResponse(data)
    else:
        messages = Chat_Messages.objects.filter(chat=chat).order_by("timestamp")
        context = {
            "chat": chat,
            "messages": messages
        }
        return render(request, "chat_messages.html", context)