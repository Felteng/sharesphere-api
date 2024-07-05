from django.urls import path
from .views import ListMessages, TargetMessage


urlpatterns = [
    path('messages/', ListMessages.as_view()),    
    path('messages/<int:pk>', TargetMessage.as_view()),    
]
