from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
import os

User = get_user_model()

def validate_unique_email(email, instance=None):
    qs = User.objects.filter(email=email)
    if instance:
        qs = qs.exclude(pk=instance.pk)
    if qs.exists():
        raise ValidationError("A user with that email already exists.")
    return email


class UserCreateForm(UserCreationForm):

    
    class Meta:
        model = User
        fields = ("username", "email", "password1")

    def clean_email(self):
        return validate_unique_email(self.cleaned_data.get("email"), self.instance)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Display Name"
        self.fields["email"].label = "Email Address"


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "profile_picture", "bio"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Display Name"
        self.fields["email"].label = "Email Address"

    def clean_email(self):
        return validate_unique_email(self.cleaned_data.get("email"), self.instance)

    def clean_profile_picture(self):
        image = self.cleaned_data.get("profile_picture")
        if image:
            valid_extensions = [".jpg", ".jpeg", ".png"]
            valid_mime_types = ["image/jpeg", "image/png"]
            ext = os.path.splitext(image.name)[1].lower()

            if ext not in valid_extensions:
                raise ValidationError("Only .jpg and .png files are allowed.")

            if hasattr(image, "content_type") and image.content_type not in valid_mime_types:
                raise ValidationError("Unsupported file type.")

        return image
  
