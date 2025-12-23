from rest_framework import serializers
from .models import Habit
from django.utils import timezone

class HabitSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Habit
        fields = '__all__'

