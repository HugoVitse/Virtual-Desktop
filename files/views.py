from django.shortcuts import render, redirect
from .forms import FileUploadForm
from .models import File
from django.contrib.auth.decorators import login_required
import os

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save(commit=False)
            file_instance.user = request.user  # On affecte l'utilisateur connecté
            file_instance.save(request.POST.get('path'))  # On enregistre le fichier
            return redirect('desktop')  # Redirige vers une page listant les fichiers (à créer)
    else:
        form = FileUploadForm()
    return render(request, 'files/upload_file.html', {'form': form})


@login_required
def mkdir(request):
    if request.method == 'POST':
        path = request.POST.get('path')
        name = request.POST.get('name')
        os.makedirs(f'media/files/{request.user.id}/{path}/{name}')
    return redirect('desktop')  # Redirige vers une page listant les fichiers (à créer)


@login_required
def file_view(request):
    files = File.objects.filter(user_id=request.user.id)  # Afficher uniquement les fichiers de l'utilisateur connecté
    return render(request, 'files/file_view.html', {'files': files})


@login_required
def update_file(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        file_id = request.POST.get('file_id')
        file = File.objects.get(id=file_id, user_id=request.user.id)

        if not file.file_type == 'txt':
            return render(request, 'files/error.html', {'message': 'Only .txt files can be updated.'})
        with open(f'media/{file.file}', 'w') as f:
            f.write(data)
        return redirect('desktop')
