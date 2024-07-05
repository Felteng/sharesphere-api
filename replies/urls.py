from django.urls import path
from .views import ListReplies, TargetReply


urlpatterns = [
    path('replies/', ListReplies.as_view()),
    path('replies/<int:pk>', TargetReply.as_view()),
]
