from django.contrib import admin
from web.messages.models import Message, MessageThread

admin.site.register(Message)
admin.site.register(MessageThread)