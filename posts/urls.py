from django.urls import path
from .views import ListPosts

urlpatterns = [
    path('posts/', ListPosts.as_view())
]