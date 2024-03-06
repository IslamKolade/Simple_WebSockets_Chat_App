from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Group_Chat, Group_Messages
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib import messages

@login_required
def join_group_chat(request):
    group_name = request.GET.get("group_name")
    
    if group_name:
        try:
            group = Group_Chat.objects.get(group_name=group_name)
            
            if group.members.count() >= 512: 
                messages.error(request, "This group is already at its maximum capacity.")
                return render(request, 'join_group_chat.html')
            
            if request.user not in group.members.all():
                group.members.add(request.user)
                messages.success(request, "Welcome to " + group.group_name + "!")
                return redirect('group_messages', url=group.url)
            else:
                messages.warning(request, "You're already a member of this group.")
                return redirect('group_messages', url=group.url)
        except Group_Chat.DoesNotExist:
            messages.error(request, "Invalid group name.")
            return render(request, 'join_group_chat.html')
    else:
        return render(request, 'join_group_chat.html')


@login_required
def create_group_chat(request):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        if group_name.strip() == '':
            return HttpResponseForbidden()
        stripped_group_name = group_name.strip()
        new_group = Group_Chat.objects.create(group_name=stripped_group_name)
        new_group.members.add(request.user)
        return redirect('group_messages', url=new_group.url)
    return render(request, 'create_group_chat.html')


@login_required
def group_messages(request, url):
    group = Group_Chat.objects.get(url=url)
    if request.user not in group.members.all():
        return HttpResponseForbidden()
    
    if request.method == "POST":
        message_sent = request.POST.get("message")
        
        message = Group_Messages.objects.create(
            group=group,
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
        messages = Group_Messages.objects.filter(group=group).order_by("timestamp")
        context = {
            "group": group,
            "messages": messages
        }
        return render(request, "group_messages.html", context)