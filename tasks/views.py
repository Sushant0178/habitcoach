from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm

@login_required
def tasks_home(request):
    # 1. Handle "Add Task" Form
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_home')
    else:
        form = TaskForm()

    # 2. Get User's Tasks (Ordered by completion status, then priority)
    tasks = Task.objects.filter(user=request.user).order_by('completed', '-priority') # Simple sorting

    return render(request, 'tasks/task_home.html', {'form': form, 'tasks': tasks})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('task_home')

@login_required
def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('task_home')