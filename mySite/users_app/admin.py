from django.contrib import admin

from .models import Message

# Register the Message model to the admin site
admin.site.register(Message)
