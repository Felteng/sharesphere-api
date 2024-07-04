from django.urls import path
from .views import ListFollowers, TargetFollower


urlpatterns = [
    path('followers/', ListFollowers.as_view()),
    path('followers/<int:pk>', TargetFollower.as_view()),
]
