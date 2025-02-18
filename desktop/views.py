# desktop/views.py
from django.shortcuts import render

def desktop_view(request):
    # Cette vue rendra le template desktop.html
    return render(request, 'desktop/desktop.html')
