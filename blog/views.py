from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .models import Post, Comment
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import NewCommentForm
from users.models import UserProfile


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
        if UserProfile.objects.filter(user=self.request.user).exists():
            current_user_profile = UserProfile.objects.get(user=self.request.user)
        else:
            current_user_profile = UserProfile(user=self.request.user)
            current_user_profile.save()
        follow = current_user_profile.follows.all().count()
        follower = UserProfile.objects.filter(follows = current_user_profile).count()
        users = User.objects.exclude(username = self.request.user.username)
        data["current_user"] = current_user_profile
        data["users"] = users
        data["follow"] = follow
        data["follower"] =follower
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
        current_user_profile = UserProfile.objects.get(user=self.request.user)
        visit_user_profile = UserProfile.objects.get(user=self.visit_user())
        #UserProfile.objects.filter(follows=current_user_profile).count()
        followers = current_user_profile.follows.all()
        print(followers.filter(user=self.visit_user()))
        if not followers.filter(user=self.visit_user()):
            already_followed = False
        else:
            already_followed = True
        print(already_followed)
        print(visit_user_profile)
        data['user'] = self.visit_user()
        data['already_followed'] = already_followed
        return data
    def post(self, request, *args, **kwargs):
        current_user_profile = UserProfile.objects.get(user=self.request.user)
        visit_user_profile = UserProfile.objects.get(user=self.visit_user())
        if request.POST['action'] == 'follow':
            current_user_profile.follows.add(visit_user_profile)
        elif request.POST['action'] == 'unfollow':
            current_user_profile.follows.remove(visit_user_profile)
        return self.get(self, request, *args, **kwargs)

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

class FollowListView(LoginRequiredMixin, generic.ListView):
    model = UserProfile
    template_name = 'blog/user_follow.html'
    # queryset = UserProfile.objects.all()
    context_object_name = 'follow_list'
    def visit_user(self):
        visit_user = get_object_or_404(User, username=self.kwargs.get('username'))
        return visit_user
    def get_queryset(self):
        current_user_profile = UserProfile.objects.get(user=self.visit_user())
        return current_user_profile.follows.all()


class FollowerListView(LoginRequiredMixin, generic.ListView):
    model = UserProfile
    template_name = 'blog/user_follower.html'
    context_object_name = "follower_list"
    def visit_user(self):
        visit_user = get_object_or_404(User, username=self.kwargs.get('username'))
        return visit_user
    def get_queryset(self):
        current_user_profile = UserProfile.objects.get(user=self.visit_user())
        return UserProfile.objects.filter(follows = current_user_profile)