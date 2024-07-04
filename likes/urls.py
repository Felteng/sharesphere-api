from django.urls import path
from .views import ListLikes, TargetLike


urlpatterns = [
    path('likes/', ListLikes.as_view()),
    path('likes/<int:pk>', TargetLike.as_view()),
]
