from django.urls import path
from . import views

urlpatterns = [
    path('', views.habit_list, name='habit_list'),
    path('add/', views.add_habit, name='add_habit'),
    path('toggle/<int:habit_id>/', views.toggle_habit_complete, name='toggle_habit'),
    path('habits/', views.habit_list, name='habits'),
]
