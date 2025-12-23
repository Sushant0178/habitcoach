from django.urls import path
from .views import TaskListCreateView,  TaskDetailsView
urlpatterns = [
    path('tasks/', TaskListCreateView.as_view()),
    path('tasks/<int:id>/', TaskDetailsView.as_view()),
]
