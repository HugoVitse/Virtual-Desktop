import subprocess
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from files.models import File

@login_required
def desktop_view(request):
    # Récupérer les fichiers de l'utilisateur connecté
    files = File.objects.filter(user_id=request.user.id)

    # Initialiser les variables pour le terminal
    output = ""
    error = ""

    if request.method == "POST":
        command = request.POST.get("command", "").strip()

        if command:  # Éviter d'exécuter une commande vide
            try:
                # Exécuter la commande shell en mode sécurisé
                result = subprocess.run(
                    command, shell=True, capture_output=True, text=True, timeout=5
                )
                output = result.stdout
                error = result.stderr
            except Exception as e:
                error = str(e)

    context = {
        "files": files,  # Affichage des fichiers de l'utilisateur
        "output": output,  # Résultat du terminal
        "error": error,  # Erreur éventuelle du terminal
    }

    return render(request, "desktop/desktop.html", context)
