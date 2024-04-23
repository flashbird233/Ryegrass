import json
from datetime import datetime, timedelta

import pandas as pd
import requests
from dateutil.relativedelta import relativedelta
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
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
    # The lat should between -33 and -40, lon should between 139 and 152
    ryegrass = Ryegrass.objects.filter(
        Q(rye_date__gte=check_date) &
        Q(rye_lat__gte=-40) &
        Q(rye_lat__lte=-33) &
        Q(rye_lon__gte=139) &
        Q(rye_lon__lte=152)
    ).values('rye_lat', 'rye_lon', 'rye_vernacular_name')
    return render(request, 'Map_Page.html', {'locations': ryegrass})


# Cloth Edu Page
def cloth_edu(request):
    return render(request, 'Cloth_Edu.html')


def base(request):
    return render(request, 'base.html')


def allergy_hub(request):
    symptoms = Symptom.objects.all()
    sample_rate_data = calculate_percentage()
    sample_rate_data_json = json.dumps(sample_rate_data)
    return render(request, 'Allergy_Hub.html', {'symptoms': symptoms, 'sampleRateData': sample_rate_data_json})


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


def symptom_relief_form(request):
    if request.method == 'POST':
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
            percentages = calculate_percentage()
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


def calculate_percentage():
    symptoms = Symptom.objects.all()
    statistics = SymptomStatistics.objects.all()

    # Calculate total count of all symptoms
    total_count = sum(statistic.symptom_count for statistic in statistics)

    # Initialize lists to store labels and data
    labels = []
    data = []

    for symptom in symptoms:
        # Find the statistic for the current symptom
        statistic = statistics.filter(symptom_id=symptom.symptom_id).first()
        # Calculate the percentage of the symptom count compared to the total count as a floating point number
        percentage = (statistic.symptom_count / total_count) * 100.0
        # Format the percentage to have one decimal place
        formatted_percentage = "{:.1f}".format(percentage)
        # Append symptom title to labels list
        labels.append(symptom.symptom_title)
        # Append formatted percentage to data list
        data.append(float(formatted_percentage))  # Convert the formatted string back to float

    # Create sample rate data dictionary
    sampleRateData = {
        'labels': labels,
        'data': data,
    }

    # If there are other symptoms not included in the statistics, calculate their total count and percentage
    if total_count < sum(symptom_count.symptom_count for symptom_count in statistics):
        other_count = sum(symptom_count.symptom_count for symptom_count in statistics) - total_count
        other_percentage = (other_count / total_count) * 100
        sampleRateData['labels'].append('Others')
        sampleRateData['data'].append(other_percentage)

    return sampleRateData


def generate_calendar_form(request):
    if request.method == 'POST':
        form = request.POST.get('data')
        form_data_array = json.loads(form)
        processed_data_list = []

        smallest_date = None
        for form_data in form_data_array:
            color = form_data['color']
            summary = form_data['summary']
            start_date = form_data['startDate']
            time = form_data['time']
            duration = int(form_data['duration'])
            end = int(form_data['end'])

            start_datetime_str = start_date + ' ' + time
            event_start = datetime.strptime(start_datetime_str, '%Y-%m-%d %H:%M')
            event_end = datetime(event_start.year, event_start.month, event_start.day, 23, 59, 0) + timedelta(days=end)

            if smallest_date is None:
                smallest_date = event_start

            if event_start < smallest_date:
                smallest_date = event_start

            iter_date = event_start
            while iter_date <= event_end:
                iter_date += timedelta(hours=duration)

                # Append processed data to the list
                processed_data_list.append({
                    'color': color,
                    'summary': summary,
                    'start': iter_date.strftime('%Y%m%dT%H%M00Z'),
                    'end': iter_date.strftime('%Y%m%dT%H%M00Z'),
                    'day': iter_date.day,
                    'time': iter_date.strftime('%H:%M'),
                })

        current_date = smallest_date
        current_month = current_date.strftime('%B %Y')

        # Determine the start day of the month (Monday being 0, Sunday being 6)
        start_day_of_month = datetime(current_date.year, current_date.month, 1).weekday()

        # Generate all days of the current month
        days_in_month = []

        # Fill in empty days at the beginning of the month
        for _ in range(start_day_of_month):
            days_in_month.append(None)

        # Generate remaining days of the current month
        first_day_of_month = datetime(current_date.year, current_date.month, 1)
        while first_day_of_month.month == current_date.month:
            days_in_month.append(first_day_of_month)
            first_day_of_month += timedelta(days=1)

        # Calculate the last day of the month
        last_day_of_month = current_date.replace(day=1) + timedelta(days=32)
        last_day_of_month = last_day_of_month.replace(day=1) - timedelta(days=1)

        # Get the weekday of the last day of the month (Monday being 0, Sunday being 6)
        weekday_of_last_day = last_day_of_month.weekday()

        # Fill in empty days at the end of the month
        for _ in range(6 - weekday_of_last_day):
            days_in_month.append(None)

        return render(request, 'reminder_calendar.html', {
            'current_month': current_month,
            'days_in_month': days_in_month,
            'events': processed_data_list
        })
    else:
        return redirect('Allergy_Hub.html')
