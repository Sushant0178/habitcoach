from django.urls import path
from .views import HabitListCreateAPI, HabitDetailAPI

urlpatterns = [
    path('habits/', HabitListCreateAPI.as_view()),
    path('habits/<int:id>/', HabitDetailAPI.as_view()),
]
