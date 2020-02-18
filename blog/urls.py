from django.urls import path, include
from . import views

urlpatterns = [
    path('posts/', views.PostView.as_view(), name='posts'),
    path('create_post/', views.PostCreateView.as_view(), name= 'create_post'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='detail' ),
    path('<int:pk>/delete_post/', views.PostDeleteView.as_view(), name='delete_post'),
]

