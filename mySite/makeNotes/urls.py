from django.urls import path
from .import views
app_name='makeNotes'

urlpatterns=[
    
  path('', views.NoteListView.as_view(), name='note_list'),
    path('new/', views.NoteCreateView.as_view(), name='note_create'),
    path('<int:pk>/edit/', views.NoteUpdateView.as_view(), name='note_edit'),
    path('<int:pk>/delete/', views.NoteDeleteView.as_view(), name='note_delete'),
 path('<int:pk>/download/', views.NoteDownloadView.as_view(), name='note_download'),
    path('upload/', views.NoteUploadView.as_view(), name='note_upload'),
]