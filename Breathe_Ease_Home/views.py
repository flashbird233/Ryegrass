import json

import pandas as pd
import requests
from dateutil.relativedelta import relativedelta
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone
from Breathe_Ease_Home.models import Ryegrass, Symptom, SymptomStatistics, SymptomRecommends, Recommend
from .forms import ExposureTimeForm, SymptomForm


# import logging
#
# logger = logging.getLogger(__name__)


def home(request):
    return render(request, 'Breathe_Ease_Home.html')


def rye_map(request):
    # Only keep last 3 years data
    now = timezone.now()
    check_date = now - relativedelta(years=3)
    ryegrass = Ryegrass.objects.filter(rye_date__gte=check_date).values('rye_lat', 'rye_lon', 'rye_vernacular_name')
    return render(request, 'Map_Page_New.html', {'locations': ryegrass})


# Cloth Edu Page
def cloth_edu(request):
    return render(request, 'Cloth_Edu.html')


def base(request):
    return render(request, 'base.html')


def allergy_hub(request):
    symptoms = Symptom.objects.all()
    return render(request, 'Allergy_Hub.html', {'symptoms': symptoms})


def update_ryegrass(request):
    ryegrass = Ryegrass.objects.all()
    response = requests.get(
        'https://api.ala.org.au/occurrences/occurrences/search?q=lsid%3Ahttps%3A%2F%2Fid.biodiversity.org.au%2Ftaxon%2Fapni%2F51442752&qualityProfile=ALA&qc=-_nest_parent_%3A*')
    response = json.loads(response.text)
    records = response['occurrences']
    new_json = []
    for record in records:
        new_rec = {'rye_lat': float(record['decimalLatitude']),
                   'rye_lon': float(record['decimalLongitude']),
                   'rye_recorded_by': " | ".join(record.get('recordedBy')),
                   'rye_date': record.get('eventDate'),
                   'rye_scientific_name': str(record.get('scientificName')),
                   'rye_vernacular_name': str(record.get('vernacularName')),
                   'rye_taxon_concept_id': str(record.get('taxonConceptID'))}
        new_json.append(new_rec)
    new_df = pd.DataFrame(new_json)
    # Remove the records with missing eventDate
    new_df = new_df[new_df['rye_date'].notna()].reset_index(drop=True)
    # Change the rye_date to datetime
    new_df['rye_date'] = pd.to_datetime(new_df['rye_date'], unit='ms')
    new_df['rye_date'] = new_df['rye_date'].dt.strftime('%Y-%m-%d')
    # Get current data
    current_df = pd.DataFrame(list(ryegrass.values()))
    # Only keep the data in new_df when rye_date, rye_lat, rye_lon are not in current_df
    current_df.set_index(['rye_lat', 'rye_lon'], inplace=True)
    new_df = new_df.merge(current_df, how='left', left_on=['rye_lat', 'rye_lon'], right_index=True,
                          indicator=True)
    new_df = new_df[new_df['_merge'] != 'both']
    new_df.drop(columns=['_merge'], inplace=True)
    # Save the new data to database
    for index, row in new_df.iterrows():
        ryegrass = Ryegrass(rye_lat=row['rye_lat'], rye_lon=row['rye_lon'],
                            rye_record_by=row['rye_recorded_by'],
                            rye_date=row['rye_date_x'],
                            rye_scientific_name=row['rye_scientific_name_x'],
                            rye_vernacular_name=row['rye_vernacular_name_x'],
                            rye_taxon_concept_id=row['rye_taxon_concept_id_x'])
    return render(request, 'Update_RyeDB.html', {'ryegrass': ryegrass})
    # return render(request, 'Update_RyeDB.html')


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
    return render(request, 'chat.html')  # 'chat.html' is the interface


def generate_calendar_form(request):
    return render(request, 'Allergy_Hub.html')


def symptom_relief_form(request):
    if request.method == 'POST':
        # selected_symptoms_ids = request.POST.getlist('symptoms')
        # symptoms = Symptom.objects.filter(id__in=selected_symptoms_ids)
        # print("POST===>>", request.POST, selected_symptoms_ids)

        form = SymptomForm(request.POST)
        if form.is_valid():
            selected_symptoms = form.cleaned_data['symptoms']
            recommend_ids = SymptomRecommends.objects.filter(symptom_id__in=selected_symptoms).values_list(
                'recommend_id', flat=True)
            recommends = Recommend.objects.filter(recommend_id__in=recommend_ids).distinct()

            # Render the result template and return as JSON
            result_html = render_to_string('recommend_template.html', {'recommends': recommends})
            return JsonResponse({'result_html': result_html})
    else:
        symptoms = Symptom.objects.all()
        form = SymptomForm()
        return render(request, 'Allergy_Hub.html', {'form': form, 'symptoms': symptoms})


def symptom_stats_form(request):
    if request.method == 'POST':
        form = SymptomForm(request.POST)
        if form.is_valid():
            selected_symptoms = form.cleaned_data['symptoms']
            update_symptom_counts(selected_symptoms)
            percentages = calculate_percentage(selected_symptoms)
            return JsonResponse({'percentages': percentages})
    else:
        form = SymptomForm()
        symptoms = Symptom.objects.all()
        return render(request, 'Allergy_Hub.html', {'form': form, 'symptoms': symptoms})


def update_symptom_counts(selected_symptoms):
    for symptom in selected_symptoms:
        symptom_stats, _ = SymptomStatistics.objects.get_or_create(symptom_id=symptom.symptom_id)
        symptom_stats.symptom_count += 1
        symptom_stats.save()


def calculate_percentage(selected_symptoms):
    # Get all symptoms
    all_symptoms = SymptomStatistics.objects.all()
    # Calculate the total count of all symptoms
    total_count = sum(symptom.symptom_count for symptom in all_symptoms)
    # Calculate the count of selected symptoms
    selected_count = sum(symptom.symptom_count for symptom in selected_symptoms)
    # Calculate the count of the rest of the symptoms
    rest_count = total_count - selected_count
    # Calculate the percentage of selected symptoms
    selected_percentage = [(symptom.symptom_count / total_count) * 100 for symptom in selected_symptoms]
    # Calculate the percentage of the rest of the symptoms as one percentage
    rest_percentage = (rest_count / total_count) * 100
    # Create labels for selected symptoms
    selected_labels = [symptom.symptom_title for symptom in selected_symptoms]
    selected_labels.append('others')  # Add 'others' label
    # Create data for selected symptoms and rest
    selected_data = selected_percentage + [rest_percentage]

    return {
        'labels': selected_labels,
        'data': selected_data,
    }
