from django.urls import path
from . import views

urlpatterns = [
    path('', views.tasks_home, name='task_home'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('toggle/<int:task_id>/', views.toggle_task, name='toggle_task'),
    path('add/', views.tasks_home, name='add_task'),

]
