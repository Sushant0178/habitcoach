from django.urls import path
from .views import MoodListCreateAPI, MoodDetailAPI

urlpatterns = [
    path('mood/', MoodListCreateAPI.as_view()),
    path('mood/<int:id>/', MoodDetailAPI.as_view()),
]
