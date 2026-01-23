from datetime import date
from habits.models import Habit
from tasks.models import Task

def get_ai_recommendation(user, mood_entry):
    """
    Analyzes user data and returns a smart suggestion.
    """
    today = date.today()
    
    # 1. Fetch Data
    pending_tasks_count = Task.objects.filter(user=user, completed=False).count()
    habits = Habit.objects.filter(user=user)
    
    # Calculate completed habits for today (this logic might vary based on your exact record keeping)
    completed_habits = 0
    for habit in habits:
        if habit.habitrecord_set.filter(date=today, completed=True).exists():
            completed_habits += 1
            
    total_habits = habits.count()
    
    # 2. The "Brain" (Rules Engine)
    recommendation = "Stay consistent! You are doing great." # Default

    # Scenario A: Bad Mood + Low Productivity
    if mood_entry and mood_entry.mood == 'Sad' and completed_habits == 0:
        recommendation = "It looks like a tough day. Don't worry about big tasks. Just try to do one small habit (like a 2-minute walk) to get a win."

    # Scenario B: Overwhelmed (Many tasks)
    elif pending_tasks_count > 5:
        recommendation = f"You have {pending_tasks_count} pending tasks. Try 'Eat the Frog' technique: Pick the hardest task and do it first, ignoring the rest for now."

    # Scenario C: High Productivity but No Mood Logged
    elif completed_habits > 0 and not mood_entry:
        recommendation = "You are productive today! Don't forget to log your mood to track how your achievements make you feel."

    # Scenario D: Streak Building
    elif completed_habits == total_habits and total_habits > 0:
        recommendation = "Perfect score today! You are building an unbreakable chain. Keep this momentum for tomorrow."

    return recommendation

# habitcoach/ai_logic.py

# from django.conf import settings
# import google.generativeai as genai


# genai.configure(api_key=settings.GEMINI_API_KEY)

# def get_chatgpt_advice(user, mood):
#     try:
#         model = genai.GenerativeModel("gemini-pro")

#         prompt = f"""
#         You are a helpful habit coach.
#         User mood today: {mood}
#         Give short, practical advice.
#         """

#         response = model.generate_content(prompt)
#         return response.text

#     except Exception as e:
#         return "AI advice is temporarily unavailable."
