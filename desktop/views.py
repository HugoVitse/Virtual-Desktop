# desktop/views.py
from django.shortcuts import render
from django.template import RequestContext
from files.forms import FileUploadForm
from files.models import File
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings
from django.http import JsonResponse
import base64


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
def desktop_view(request):
    # Cette vue rendra le template desktop.html
    form = FileUploadForm()
    files = File.objects.filter(user_id=request.user.id)  # Afficher uniquement les fichiers de l'utilisateur connecté
    return render(request, 'desktop/desktop.html', {'files': files, 'form': form})


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



