# desktop/views.py
from django.shortcuts import render
from files.models import File
from django.contrib.auth.decorators import login_required


@login_required
def desktop_view(request):
    # Cette vue rendra le template desktop.html
    files = File.objects.filter(user_id=request.user.id)  # Afficher uniquement les fichiers de l'utilisateur connecté
    return render(request, 'desktop/desktop.html', {'files': files})
