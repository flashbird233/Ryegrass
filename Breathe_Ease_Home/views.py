# Breathe_Ease_Home/views.py

from django.shortcuts import render

from Breathe_Ease_Home.models import Ryegrass


def home(request):
    return render(request, 'Breathe_Ease_Home.html')


def rye_map(request):
    # Get ryegrass locations from database
    ryegrass = Ryegrass.objects.all()
    return render(request, 'Map_Page.html', {'locations': locations})
