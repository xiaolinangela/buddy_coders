from django.shortcuts import render, redirect
from django.views import generic
from .models import Post
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.


def home(request):
    return redirect('blog/posts')

class PostView(LoginRequiredMixin, generic.ListView):
    template_name = 'blog/posts.html'
    queryset = Post.objects.all()
    context_object_name = 'latest_blog_list'

class PostCreateView(CreateView):
    model = Post
    fields = ['content']
    template_name = 'blog/create_post.html'
    success_url = '/'
    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        return data

class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blog/detail.html'

class PostDeleteView(generic.DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'
    success_url = '/'

