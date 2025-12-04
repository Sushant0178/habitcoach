from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Habit
from .forms import HabitForm



@login_required
def add_habit(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            return redirect('habit_list')
    else:
        form = HabitForm()
    return render(request, 'habits/add_habit.html', {'form': form})

from django.utils import timezone
from .models import Habit, HabitRecord

@login_required
def habit_list(request):
    habits = Habit.objects.filter(user=request.user)
    today = timezone.now().date()

    # Prepare habit records dictionary
    habit_records = {}
    for habit in habits:
        record, _ = HabitRecord.objects.get_or_create(habit=habit, date=today)
        habit_records[habit.id] = record

    return render(request, 'habits/habit_list.html', {
        'habits': habits,
        'habit_records': habit_records,
    })

@login_required
def toggle_habit_complete(request, habit_id):
    from django.http import HttpResponseRedirect
    habit = Habit.objects.get(id=habit_id, user=request.user)
    today = timezone.now().date()
    record, created = HabitRecord.objects.get_or_create(habit=habit, date=today)
    record.completed = not record.completed
    record.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
