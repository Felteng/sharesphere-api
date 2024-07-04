from django.urls import path
from .views import ListProfiles, TargetProfile

urlpatterns = [
    path('profiles/', ListProfiles.as_view()),
    path('profiles/<int:pk>/', TargetProfile.as_view()),
]
