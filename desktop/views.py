from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime

@login_required
def desktop_view(request):
    # On peut également ajouter d'autres éléments dynamiques ici, comme des notifications, etc.
    current_time = datetime.now().strftime("%H:%M:%S")  # Obtenir l'heure actuelle
    show_agenda = request.GET.get('show_agenda', 'false') == 'true'


    context = {
        "current_time": current_time,
        'show_agenda': show_agenda,
    }
    
    return render(request, 'desktop/desktop.html', context)
