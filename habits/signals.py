from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Habit, HabitRecord
from notifications.models import Badge, Notification

# Existing signal (keep this)
@receiver(post_save, sender=Habit)
def create_today_record(sender, instance, created, **kwargs):
    if created:
        today = timezone.now().date()
        HabitRecord.objects.get_or_create(habit=instance, date=today)

# --- NEW: Badge Logic ---
@receiver(post_save, sender=HabitRecord)
def check_for_badges(sender, instance, **kwargs):
    """
    Checks if a badge should be awarded when a habit is completed.
    """
    if instance.completed:
        user = instance.habit.user
        habit = instance.habit
        streak = habit.current_streak()
        
        # Define Milestones
        badge_name = None
        if streak == 3:
            badge_name = "Bronze Streak (3 Days)"
        elif streak == 7:
            badge_name = "Silver Streak (7 Days)"
        elif streak == 30:
            badge_name = "Gold Streak (30 Days)"

        # Award Badge if earned and not already owned
        if badge_name:
            if not Badge.objects.filter(user=user, name=badge_name).exists():
                Badge.objects.create(
                    user=user, 
                    name=badge_name, 
                    earned_on=timezone.now().date()
                )
                
                # Notify User
                Notification.objects.create(
                    user=user,
                    message=f"🏆 Congrats! You earned the '{badge_name}' badge for {habit.name}!"
                )