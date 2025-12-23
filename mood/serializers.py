from rest_framework import serializers
from .models import Mood


class MoodSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Mood
        fields = '__all__'