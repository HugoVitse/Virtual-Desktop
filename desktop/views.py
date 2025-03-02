import shlex
import subprocess
from django.shortcuts import render, redirect
from django.template import RequestContext
from files.forms import FileUploadForm
from files.models import File
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings
from django.http import JsonResponse
import base64
from .models import Task
from datetime import datetime
from dateutil import parser

@login_required
def file(request):
    user_id = request.user.id  # Récupère l'ID de l'utilisateur connecté
    file_id = request.GET.get('file_id', '')  # ID du fichier demandé par l'utilisateur

    try:
        file = File.objects.get(id=file_id, user_id=user_id)
    except File.DoesNotExist:
        return JsonResponse({'error': 'Fichier introuvable'}, status=404)

    full_path = os.path.join(settings.MEDIA_ROOT, file.file.path)

    if not os.path.exists(full_path) or not os.path.isfile(full_path):
        return JsonResponse({'error': 'Fichier introuvable'}, status=404)

    with open(full_path, 'rb') as f:
        file_data = f.read()

    file_data_base64 = base64.b64encode(file_data).decode('utf-8') if file.file_type =='image'  else file_data.decode('utf-8')
    response = JsonResponse({'file_name': os.path.basename(full_path), 'file_data': file_data_base64})
    return response



@login_required
def list_directory(request):
    user_id = request.user.id  # Récupère l'ID de l'utilisateur connecté
    base_path = os.path.join(settings.MEDIA_ROOT, 'files', str(user_id))  # Chemin de base
    requested_path = request.GET.get('path', '')  # Chemin demandé par l'utilisateur

    full_path = os.path.join(base_path, requested_path)

    if not os.path.exists(full_path):
        return JsonResponse({'error': 'Dossier introuvable'}, status=404)

    files = []
    folders = []

    for item in os.listdir(full_path):
        item_path = os.path.join(full_path, item)
        relative_path = os.path.join(requested_path, item)  # Chemin relatif depuis `media/files/<user_id>/`

        if os.path.isdir(item_path):
            folders.append({'name': item, 'path': relative_path, 'is_dir': True})
        else:
            try:
                file_obj = File.objects.get(file=os.path.join('files', str(user_id), relative_path))
                file_id = file_obj.id
                file_type = 'img' if item.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')) else 'txt' if item.lower().endswith('.txt') else 'other'
            except File.DoesNotExist:
                file_id = None
                file_type = 'other'
            files.append({'name': item, 'path': relative_path, 'is_dir': False, 'id': file_id, 'type': file_type})

    return JsonResponse({'folders': folders, 'files': files})



from django.contrib.auth.decorators import login_required
from files.models import File

@login_required
def desktop_view(request):
    # Récupérer les fichiers de l'utilisateur connecté
    files = File.objects.filter(user_id=request.user.id)
    form = FileUploadForm()

    # Initialiser les variables pour le terminal
    output = ""
    error = ""

    current_time = datetime.now()
    tasks = Task.objects.all()

    ALLOWED_COMMANDS = {"ls", "cat", "echo", "touch", "rm", "mkdir", "rmdir"}

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
                

        user_id = request.user.id  # Supposons que l'utilisateur soit authentifié
        user_dir = os.path.abspath(f"media/files/{user_id}/")  

        # Vérifier que le dossier existe, sinon refuser l'exécution
        if not os.path.exists(user_dir):
            return JsonResponse({"error": "Répertoire utilisateur introuvable"}, status=400)

        command = request.POST.get("command", "").strip()

        if not command:
            return JsonResponse({"error": "Commande vide non autorisée"}, status=400)

        try:
            # Séparer proprement la commande en liste
            command_list = shlex.split(command)
            if command_list[0] not in ALLOWED_COMMANDS:
                throw_error = f"Commande non autorisée: {command_list[0]}"
                raise Exception(throw_error)
            
            for arg in command_list[1:]:
                if os.path.isabs(arg) or ".." in arg:
                    throw_error = f"Argument non autorisé: {arg}"
                    raise Exception(throw_error)

                # Convertir le chemin en absolu et vérifier qu'il est bien dans user_dir
                arg_path = os.path.abspath(os.path.join(user_dir, arg))
                if not arg_path.startswith(user_dir):
                    throw_error = f"Argument non autorisé: {arg}"
                    raise Exception(throw_error)

            # Exécuter uniquement dans le dossier de l'utilisateur
            result = subprocess.run(
                command_list,
                cwd=user_dir,  # Forcer l'exécution dans le répertoire autorisé
                capture_output=True,
                text=True,
                timeout=5
            )

            
            output = result.stdout
            
        except Exception as e:
            error = str(e)

    context = {
        "files": files,  # Affichage des fichiers de l'utilisateur
        "output": output,  # Résultat du terminal
        "error": error,  # Erreur éventuelle du terminal
        "form":form
    }

    return render(request, "desktop/desktop.html", context)

