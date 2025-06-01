
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth import get_user_model,logout

from . import forms
user=get_user_model()

class SignUp(CreateView):
    form_class = forms.UserCreateForm  # ✅ fixed typo here
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')  # or any other page you'd prefer
        return super().dispatch(request, *args, **kwargs)
    
class EditPage(LoginRequiredMixin, UpdateView):
   
    form_class = forms.UserUpdateForm  # You need to define this form
    template_name = 'accounts/edit.html'
    success_url = reverse_lazy('home')  # Redirect after saving changes

    def get_object(self, queryset=None):
        return self.request.user  # Ensure users can only edit themselves

class DeletePage(LoginRequiredMixin, DeleteView):
    model = user
    template_name = 'accounts/delete.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        logout(request)  # Log out before deleting the user
        return super().delete(request, *args, **kwargs)

