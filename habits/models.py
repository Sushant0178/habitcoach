from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def current_streak(self):
        """Return the number of consecutive days habit is completed up to today."""
        today = timezone.now().date()
        streak = 0
        delta = 0

        while True:
            check_date = today - timedelta(days=delta)
            record = self.habitrecord_set.filter(date=check_date, completed=True).first()
            if record:
                streak += 1
            else:
                break
            delta += 1

        return streak



class HabitRecord(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.habit.name} - {self.date}"

from django.utils import timezone

def today_completed(habit):
    today = timezone.now().date()
    record = habit.habitrecord_set.filter(date=today, completed=True).first()
    return bool(record)
