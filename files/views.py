from django.shortcuts import render, redirect
from .forms import FileUploadForm
from .models import File
from django.contrib.auth.decorators import login_required

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save(commit=False)
            file_instance.user = request.user  # On affecte l'utilisateur connecté
            file_instance.save()
            return redirect('desktop')  # Redirige vers une page listant les fichiers (à créer)
    else:
        form = FileUploadForm()
    return render(request, 'files/upload_file.html', {'form': form})

@login_required
def file_view(request):
    files = File.objects.filter(user_id=request.user.id)  # Afficher uniquement les fichiers de l'utilisateur connecté
    return render(request, 'files/file_view.html', {'files': files})
