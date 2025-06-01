from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Note
from .forms import NoteForm
from django.http import HttpResponse
from django.views.generic.edit import FormView
from .forms import UploadFileForm
from django.views import View


from django.shortcuts import get_object_or_404

class NoteListView(ListView):
    model = Note
    template_name = 'makeNotes/note_list.html'
    context_object_name = 'notes'
    ordering = ['-updated_at']

class NoteCreateView(CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'makeNotes/note_form.html'
    success_url = reverse_lazy('makeNotes:note_list')

    def form_valid(self, form):
        if not form.cleaned_data['title']:
            form.instance.title = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        return super().form_valid(form)

class NoteUpdateView(UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'makeNotes/note_form.html'
    success_url = reverse_lazy('makeNotes:note_list')

    def form_valid(self, form):
        if not form.cleaned_data['title']:
            form.instance.title = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        return super().form_valid(form)

class NoteDeleteView(DeleteView):
    model = Note
    template_name = 'makeNotes/note_confirm_delete.html'
    success_url = reverse_lazy('makeNotes:note_list')

class NoteDownloadView(View):
    def get(self, request, pk):
        note = get_object_or_404(Note, pk=pk)
        if not note.content.strip():
            return HttpResponse('This note is empty and cannot be downloaded.', status=400)

        response = HttpResponse(note.content, content_type='text/plain')
        filename = f"{note.title or note.created_at.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    
class NoteUploadView(FormView):
    template_name = 'makeNotes/note_upload.html'
    form_class = UploadFileForm
    success_url = reverse_lazy('makeNotes:note_list')

    def form_valid(self, form):
        uploaded_file = self.request.FILES['file']
        # Ensure the file is a .txt
        if not uploaded_file.name.endswith('.txt'):
            form.add_error('file', 'Only .txt files are allowed.')
            return self.form_invalid(form)

        content = uploaded_file.read().decode('utf-8')
        # Check for empty content
        if not content.strip():
            form.add_error('file', 'The file is empty.')
            return self.form_invalid(form)

        # Create the note
        title = uploaded_file.name.replace('.txt', '')
        Note.objects.create(title=title, content=content)
        return super().form_valid(form)
    


