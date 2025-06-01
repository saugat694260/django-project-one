from django.urls import path
from . import views

urlpatterns = [
    path('blogs/', views.HomeView.as_view(), name='blog-home'),
    path('my-posts/', views.MyPostView.as_view(), name='my-posts'),
    path('saved/', views.SavedPostView.as_view(), name='saved-posts'),
    path('add/', views.AddPostView.as_view(), name='add-post'),
    path('edit/<int:pk>/', views.EditPostView.as_view(), name='edit-post'),
    path('delete/<int:pk>/', views.DeletePostView.as_view(), name='delete-post'),
    path('like/<int:pk>/', views.LikePostView.as_view(), name='like-post'),
    path('save/<int:pk>/', views.SavePostView.as_view(), name='save-post'),
]
