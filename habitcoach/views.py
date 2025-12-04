from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from habits.models import Habit, HabitRecord
from mood.models import Mood
from tasks.models import Task
from .ai_logic import get_ai_recommendation  # Import our new AI logic
from datetime import timedelta # Add this import at the top
from notifications.models import Badge  # Import Badge model
from django.conf import settings
print(settings.DATABASES)

def home_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'index.html')

from datetime import timedelta # Add this import at the top

@login_required
def dashboard_view(request):  
    user = request.user
    today = timezone.now().date()

    # --- Existing Habit Logic ---
    habits = Habit.objects.filter(user=user)
    habit_data = []
    for habit in habits:
        is_completed = HabitRecord.objects.filter(habit=habit, date=today, completed=True).exists()
        habit_data.append({
            'habit': habit,
            'completed': is_completed
        })

    # --- Existing Mood/Task Logic ---
    try:
        todays_mood = Mood.objects.get(user=user, date=today)
    except Mood.DoesNotExist:
        todays_mood = None

    tasks = Task.objects.filter(user=user, completed=False).order_by('deadline')[:3]
    ai_advice = get_ai_recommendation(user, todays_mood)
    
    # --- NEW: Fetch Badges ---
    badges = Badge.objects.filter(user=user).order_by('-earned_on')

    # --- NEW: Prepare Chart Data (Last 7 Days Mood) ---
    dates = []
    mood_scores = []
    
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        dates.append(d.strftime("%a")) # Mon, Tue, etc.
        
        # Convert Mood text to Number for the Chart
        mood_entry = Mood.objects.filter(user=user, date=d).first()
        if mood_entry:
            if mood_entry.mood == 'Happy': score = 3
            elif mood_entry.mood == 'Normal': score = 2
            else: score = 1 # Sad
        else:
            score = 0 # No entry
        mood_scores.append(score)

    context = {
        'habit_data': habit_data,
        'todays_mood': todays_mood,
        'tasks': tasks,
        'ai_advice': ai_advice,
        'badges': badges,       # Pass badges
        'chart_dates': dates,   # Pass chart dates
        'chart_moods': mood_scores, # Pass chart data
    }
    return render(request, 'dashboard.html', context)