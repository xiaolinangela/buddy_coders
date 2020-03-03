from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .models import Post, Comment
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import NewCommentForm
from users.models import Follow, Profile


# Create your views here.


def home(request):
    return redirect('blog/posts')

class PostView(LoginRequiredMixin, generic.ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'blog/posts.html'
    queryset = Post.objects.all()
    context_object_name = 'latest_blog_list'

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        users = User.objects.exclude(username = self.request.user.username)
        data["users"] = users
        return data

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['content']
    template_name = 'blog/create_post.html'
    success_url = '/'
    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        return data

class PostDetailView(LoginRequiredMixin,generic.DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        comments_connected = Comment.objects.filter(post_connected=self.get_object())
        data['comments'] = comments_connected
        data['form'] = NewCommentForm(instance=self.request.user)
        return data

    def post(self, request,*args, **kwargs):
        new_comment = Comment(content=request.POST.get('content'),
                              user=self.request.user,
                              post_connected=self.get_object())
        new_comment.save()
        return self.get(self, request, *args, **kwargs)

class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'
    success_url = '/'

# class UserPostListView(LoginRequiredMixin, generic.DetailView):
#     model = Post
#     template_name = 'blog/user_detail.html'
#     def get_object(self):
#         visit_user = get_object_or_404(User, username=self.kwargs.get('username'))
#         return visit_user
#     def get_context_data(self, **kwargs):
#         data = super().get_context_data(**kwargs)
#         user = self.get_object()
#         data["user_blog_lists"] = Post.objects.filter(user=user)
#         return data


class UserPostListView(LoginRequiredMixin, generic.ListView):
    model = Post
    template_name = 'blog/user_detail.html'
    context_object_name = 'user_blog_lists'
    def visit_user(self):
        visit_user = get_object_or_404(User, username=self.kwargs.get('username'))
        return visit_user
    def get_queryset(self):
        return Post.objects.filter(user=self.visit_user())
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['user'] = self.visit_user()
        return data

class UserPostDetailView(LoginRequiredMixin, generic.DetailView):
    model = Post
    template_name = 'blog/user_post_detail.html'
    def visit_user(self):
        visit_user = get_object_or_404(User, username=self.kwargs.get('username'))
        return visit_user
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        comments_connected = Comment.objects.filter(post_connected=self.get_object())
        data['comments'] = comments_connected
        data['form'] = NewCommentForm(instance=self.visit_user())
        return data

    def post(self, request,*args, **kwargs):
        new_comment = Comment(content=request.POST.get('content'),
                              user=self.request.user,
                              post_connected=self.get_object())
        new_comment.save()
        return self.get(self, request, *args, **kwargs)
#

