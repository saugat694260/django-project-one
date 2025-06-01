from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter note title (optional)'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your note here...', 'rows': 10}),
        
        }

class UploadFileForm(forms.Form):
    file = forms.FileField(label='Upload .txt file')
