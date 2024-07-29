from django.urls import path
from .views import ListMessages, TargetMessage


urlpatterns = [
    path('messages/', ListMessages.as_view(), name='list_messages'),
    path('messages/<int:pk>', TargetMessage.as_view(), name='target_message'),
]
