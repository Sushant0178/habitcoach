from django.db import models
from django.contrib.auth.models import User

class Mood(models.Model):
    MOOD_CHOICES = [
        ('Happy', 'Happy'),
        ('Normal', 'Normal'),
        ('Sad', 'Sad')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mood = models.CharField(max_length=10, choices=MOOD_CHOICES)
    date = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.mood}"
