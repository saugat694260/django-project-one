from django.contrib.auth import get_user_model
from django.views.generic import ListView, TemplateView
from django.db.models import Q  # Import Q
from .models import Message
from django.http import Http404
from django.shortcuts import render, redirect

User = get_user_model()

class UserList(ListView):
    model = User
    template_name = 'users_app/users_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        # Get all users except the currently logged-in user
        return User.objects.exclude(id=self.request.user.id)
    
class UserMessages(TemplateView):
    template_name = 'users_app/messages.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the recipient user based on the URL
        recipient_username = self.kwargs.get('username')
        recipient = User.objects.filter(username=recipient_username).first()

        if not recipient:
            raise Http404("User not found")

        # Get all messages between the logged-in user and the recipient
        messages = Message.objects.filter(
            (Q(sender=self.request.user) & Q(recipient=recipient)) |
            (Q(sender=recipient) & Q(recipient=self.request.user))
        ).order_by('timestamp')

        context['recipient'] = recipient
        context['messages'] = messages
        return context

    def post(self, request, *args, **kwargs):
        recipient_username = self.kwargs.get('username')
        recipient = User.objects.filter(username=recipient_username).first()

        if not recipient:
            raise Http404("User not found")

        text = request.POST.get('message_text')

        if text:
            # Save the new message in the database
            message = Message.objects.create(
                sender=request.user,
                recipient=recipient,
                text=text
            )

        return redirect('users_app:user_messages', username=recipient_username)
