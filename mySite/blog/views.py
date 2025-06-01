from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import BlogPost
from .forms import BlogPostForm
from django.http import JsonResponse


# Create your views here.

class HomeView(ListView):
    model=BlogPost
    template_name='blog/blog_home.html'
    context_object_name='posts'
    ordering=['-created_at']

class MyPostView(LoginRequiredMixin,ListView):
    model=BlogPost
    template_name='blog/my_posts.html'
    context_object_name='posts'

    def get_queryset(self):
        return BlogPost.objects.filter(author=self.request.user)
    
class SavedPostView(LoginRequiredMixin,ListView):
    model=BlogPost
    template_name='blog/saved_posts.html'
    context_object_name='posts'

    def get_queryset(self):
        return self.request.user.saved_posts.all()
    
class AddPostView(LoginRequiredMixin,CreateView):
    model=BlogPost
    form_class=BlogPostForm
    template_name='blog/post_form.html'
    success_url=reverse_lazy('my-posts')

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)
    
class EditPostView(LoginRequiredMixin, UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('my-posts')

    def get_queryset(self):
        return BlogPost.objects.filter(author=self.request.user)
    
class DeletePostView(LoginRequiredMixin, DeleteView):
    model = BlogPost
    template_name = 'blog/confirm_delete.html'
    success_url = reverse_lazy('my-posts')

    def get_queryset(self):
        return BlogPost.objects.filter(author=self.request.user)
    
class LikePostView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(BlogPost, pk=pk)
        liked = False

        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
            liked = True

        return JsonResponse({
            'liked': liked,
            'like_count': post.likes.count()
        })
    
class SavePostView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(BlogPost, pk=pk)
        saved = False

        if request.user in post.saved_by.all():
            post.saved_by.remove(request.user)
        else:
            post.saved_by.add(request.user)
            saved = True

        return JsonResponse({
            'saved': saved
        })




