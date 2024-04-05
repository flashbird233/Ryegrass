# Breathe_Ease_Home/views.py

from dateutil.relativedelta import relativedelta
from django.shortcuts import render
from django.utils import timezone

from Breathe_Ease_Home.models import Ryegrass


def home(request):
    return render(request, 'Breathe_Ease_Home.html')


def rye_map(request):
    # Only keep last 3 years data
    now = timezone.now()
    check_date = now - relativedelta(years=3)
    ryegrass = Ryegrass.objects.filter(rye_date__gte=check_date).values('rye_lat', 'rye_lon', 'rye_vernacular_name')
    return render(request, 'Map_Page.html', {'locations': ryegrass})
