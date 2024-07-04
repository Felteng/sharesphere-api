from django.urls import path
from .views import ListComments, TargetComment


urlpatterns = [
    path('comments/', ListComments.as_view()),
    path('comments/<int:pk>', TargetComment.as_view()),
]
