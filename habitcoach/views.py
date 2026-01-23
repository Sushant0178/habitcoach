from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from habits.models import Habit, HabitRecord
from mood.models import Mood
from tasks.models import Task
# from .ai_logic import get_chatgpt_advice  # Import our new AI logic
from datetime import timedelta # Add this import at the top
from notifications.models import Badge  # Import Badge model
from django.conf import settings
from .ai_logic import get_ai_recommendation


def home_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'index.html')


@login_required
def dashboard_view(request):
    user = request.user
    today = timezone.now().date()

    # ---- Habits ----
    habits = Habit.objects.filter(user=user)
    habit_data = []

    for habit in habits:
        is_completed = HabitRecord.objects.filter(
            habit=habit,
            date=today,
            completed=True
        ).exists()

        habit_data.append({
            'habit': habit,
            'completed': is_completed
        })

    # ---- Mood ----
    todays_mood = Mood.objects.filter(user=user, date=today).first()

    # ---- Tasks ----
    tasks = Task.objects.filter(
        user=user,
        completed=False
    ).order_by('deadline')[:3]

    # ---- Badges / Achievements ----
    badges = Badge.objects.filter(user=user).order_by('-earned_on')

    # ---- Mood Chart (Last 7 Days) ----
    dates = []
    mood_scores = []

    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        dates.append(d.strftime("%a"))

        mood_entry = Mood.objects.filter(user=user, date=d).first()
        if mood_entry:
            if mood_entry.mood == 'Happy':
                score = 3
            elif mood_entry.mood == 'Normal':
                score = 2
            else:
                score = 1
        else:
            score = 0

        mood_scores.append(score)

    context = {
        'habit_data': habit_data,
        'todays_mood': todays_mood,
        'tasks': tasks,
        'badges': badges,
        'chart_dates': dates,
        'chart_moods': mood_scores,
    }

    return render(request, 'dashboard.html', context)


# from .ai_logic import get_chatgpt_advice
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render
# from django.utils import timezone
# from mood.models import Mood




# @login_required
# def dashboard_view(request):
#     # existing logic
#     user = request.user
#     today = timezone.now().date()
    
#     # Fetch today's mood entry
#     mood_entry = Mood.objects.filter(user=user, date=today).first()
#     todays_mood = mood_entry.mood_score if mood_entry else None
    
#     ai_advice = get_chatgpt_advice(request.user, todays_mood)

#     context = {
#         "ai_advice": ai_advice,
#         # other data
#     }
#     return render(request, "dashboard.html", context)
