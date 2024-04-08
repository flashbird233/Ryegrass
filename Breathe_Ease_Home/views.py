from dateutil.relativedelta import relativedelta
from django.shortcuts import render
from django.utils import timezone

from Breathe_Ease_Home.models import Ryegrass
from .forms import ExposureTimeForm


def home(request):
    return render(request, 'Breathe_Ease_Home.html')


def rye_map(request):
    # Only keep last 3 years data
    now = timezone.now()
    check_date = now - relativedelta(years=3)
    ryegrass = Ryegrass.objects.filter(rye_date__gte=check_date).values('rye_lat', 'rye_lon', 'rye_vernacular_name')
    return render(request, 'Map_Page.html', {'locations': ryegrass})


# Cloth Edu Page
def cloth_edu(request):
    return render(request, 'Cloth_Edu.html')


def base(request):
    return render(request, 'base.html')


def update_ryegrass(request, pk):
    ryegrass = Ryegrass.objects.get(pk=pk)
    # Your logic to update the Ryegrass object
    # ...
    return render(request, 'Update_RyeDB.html', {'ryegrass': ryegrass})


def generate_suggestions(duration):
    try:
        # Attempt to convert duration to an integer
        duration = int(duration)
    except ValueError:
        # Return an error message if the conversion fails
        return "Please enter a valid number."

    if duration <= 0:
        return "No protective measures are necessary."
    elif duration < 1:
        return "Recommend wearing a surgical mask, sunglasses, long sleeves, trousers, and a hat. Choose tightly woven cotton or synthetic fabrics."
    elif duration < 5:
        return (
            "Recommend wearing an N95 mask, sunglasses, long sleeves, trousers, gloves, and a hat. Post-exposure, it's advised to wash promptly. Opt for high-performance textiles like microporous materials or specially treated fabrics.")
    else:
        return (
            "Advise using an N95 mask, sunglasses, long sleeves, trousers, gloves, and a hat with a substantial brim. After leaving the allergen area, take a shower and change clothes immediately. For clothing material, medical-grade protective garments are preferred.")


def suggest_clothing(request):
    if request.method == 'POST':
        form = ExposureTimeForm(request.POST)
        if form.is_valid():
            suggestions = generate_suggestions(form.cleaned_data['duration'])
            return render(request, 'Cloth_Sug.html', {'suggestions': suggestions})
    else:
        form = ExposureTimeForm()

    return render(request, 'Cloth_Sug.html', {'form': form})


def customer_support_chat(request):
    return render(request, 'Chat.html')  # 'chat.html' is the interface
