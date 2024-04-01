# Breathe_Ease_Home/views.py

from django.shortcuts import render


def home(request):
    return render(request, 'Breathe_Ease_Home.html')
