from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Task
from django.contrib.auth.decorators import login_required
from datetime import datetime
from dateutil import parser

@login_required
def desktop_view(request):
    current_time = datetime.now()
    tasks = Task.objects.all()

    if request.method == "POST":
        if "add_task" in request.POST:  # Ajouter une tâche
            title = request.POST.get("title")
            description = request.POST.get("description")
            due_date_str = request.POST.get("due_date")

            if not title or not description or not due_date_str:
                return render(request, 'desktop/desktop.html', {
                    "error": "Tous les champs sont obligatoires", 
                    "current_time": current_time, 
                    "tasks": tasks
                })

            try:
                due_date = parser.parse(due_date_str)
                Task.objects.create(title=title, description=description, due_date=due_date)
                return redirect('desktop')  
            except (ValueError, TypeError):
                return render(request, 'desktop/desktop.html', {
                    "error": "Format de date invalide.", 
                    "current_time": current_time, 
                    "tasks": tasks
                })

        elif "delete_task" in request.POST:  # Supprimer une tâche
            task_id = request.POST.get("task_id")
            if task_id:  # Vérifier si un ID est bien fourni
                try:
                    task = Task.objects.get(id=int(task_id))  # Convertir l'ID en entier
                    task.delete()
                    return redirect('desktop')  
                except (Task.DoesNotExist, ValueError):
                    return render(request, 'desktop/desktop.html', {
                        "error": "Tâche introuvable.", 
                        "current_time": current_time, 
                        "tasks": tasks
                    })

    context = {
        "current_time": current_time,
        "tasks": tasks
    }
    return render(request, 'desktop/desktop.html', context)