from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Mood
from .forms import MoodForm

@login_required
def mood_home(request):
    today = timezone.now().date()
    
    # Check if mood already logged today
    already_logged = Mood.objects.filter(user=request.user, date=today).exists()

    if request.method == 'POST':
        form = MoodForm(request.POST)
        if form.is_valid():
            # Delete existing mood for today if any (to allow updates)
            Mood.objects.filter(user=request.user, date=today).delete()
            
            mood_instance = form.save(commit=False)
            mood_instance.user = request.user
            mood_instance.date = today
            mood_instance.save()
            return redirect('dashboard') # Go back to dashboard after logging
    else:
        form = MoodForm()

    return render(request, 'mood/mood_home.html', {
        'form': form, 
        'already_logged': already_logged
    })