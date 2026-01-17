from django.db.models.signals import post_save 
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in , user_logged_out, user_login_failed 
from .models import UserProfile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


# def login_success(sender, request, user, **kwargs):
#     print(f"User {user.username} logged in successfully.")

# user_logged_in.connect(login_success)

# not very useful but for demonstration

@receiver(user_logged_in)
def login_success(sender, request, user, **kwargs):          #-------------------------- usseful for security auditing 
    print(f"User {user.username} logged in successfully.")
              

