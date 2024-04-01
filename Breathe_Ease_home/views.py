# Breathe_Ease_home/views.py

from django.shortcuts import render

def home(request):
    return render(request, 'Breathe_Ease_home/home.html')
