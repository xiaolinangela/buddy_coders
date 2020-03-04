from django.urls import path, include
from . import views

urlpatterns = [
    path('posts/', views.PostView.as_view(), name='posts'),
    path('create_post/', views.PostCreateView.as_view(), name= 'create_post'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='detail' ),
    path('<int:pk>/delete_post/', views.PostDeleteView.as_view(), name='delete_post'),
    path('user/<str:username>/', views.UserPostListView.as_view(), name='user_posts'),
    path('user/<str:username>/<int:pk>/', views.UserPostDetailView.as_view(), name='user_post_detail'),
    path('user/<str:username>/following/', views.FollowListView.as_view(), name='user_following'),
    path('user/<str:username>/follower/', views.FollowerListView.as_view(), name='user_follower'),
]

