from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('authentication.urls')),
    path("accounts/", include("django.contrib.auth.urls")),
    path('', include('authentication.urls')),
    path('chat/', include('simple_chat_app.urls')),
    path('group_chat/', include('simple_groupchat_app.urls')),
]
