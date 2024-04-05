# Breathe_Ease/views.py

from django.shortcuts import render


def home(request):
    return render(request, 'Breathe_Ease_Home.html')


def rye_map(request):
    locations = [
        {'name': 'Location 1', 'lat': '-34.397', 'lng': '150.644'},
        {'name': 'Location 2', 'lat': '-30.363', 'lng': '140.044'}
    ]
    return render(request, 'Map_Page.html', {'locations': locations})
