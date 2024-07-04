from django.urls import path
from .views import ListPosts, TargetPost

urlpatterns = [
    path('posts/', ListPosts.as_view()),
    path('posts/<int:pk>/', TargetPost.as_view())
]