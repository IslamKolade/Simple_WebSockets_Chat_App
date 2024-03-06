from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from simple_groupchat_app.models import Group_Chat
from simple_chat_app.models import Chat


def home(request):
    if request.user.is_authenticated:
        group_chats = Group_Chat.get_group_chats(request.user)
        chats = Chat.get_chats(request.user)
        return render(request, "home.html", {"chats": chats, "group_chats":group_chats})
    return render(request, "home.html")


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"