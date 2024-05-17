import json
from datetime import datetime, timedelta
from math import sqrt

import pandas as pd
import requests
from dateutil.relativedelta import relativedelta
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from geopy import Point
from geopy.distance import distance

from Breathe_Ease_Home.models import Ryegrass, Symptom, SymptomStatistics, SymptomRecommends, Recommend
from .forms import ExposureTimeForm, SymptomForm


def login_view(request):
    if request.method == 'POST':
        password = request.POST.get('password', '')
        if password == 'Qwertyui!@#':  # 这是你的硬编码密码
            request.session['is_logged_in'] = True
            return redirect('home')  # 确保你有一个名为'homepage'的URL名称
        else:
            return render(request, 'login.html', {'error_message': 'Invalid password. Please try again.'})
    return render(request, 'login.html')


def home(request):
    if request.session.get('is_logged_in'):
        # print('aaaaaaaaaaaaa')
        return render(request, 'Breathe_Ease_Home.html')
    else:
        # print('bbbbbbbbbbbbb')
        return redirect('login')

    # if request.session.get('is_logged_in'):
    #     return render(request, 'Map_Page.html')
    # else:
    #     return redirect('login')


def rye_map(request):
    if request.session.get('is_logged_in'):
        return render(request, 'Map_Page.html')
    else:
        return redirect('login')


# Get the current weather of Mel by using the OpenWeatherMap API
def get_weather_cur():
    # Melbourne coordinates
    lat = -37.813611
    lon = 144.963056
    # API key and URL
    key = "d32542473437f300dfdec104552b7f65"
    main_url = "https://api.openweathermap.org/data/3.0/onecall?"
    req_url = main_url + "lat=" + str(lat) + "&lon=" + str(lon) + "&appid=" + key
    # Get the response
    response = requests.get(req_url).json()
    # Get current month
    current_month = timezone.now().month
    # Filter the response and return the required data
    return {"temp": response["current"]['temp'],  # Kelvin
            "humidity": response["current"]['humidity'],
            'wind_speed': response["current"]['wind_speed'],  # m/s
            'wind_deg': response["current"]['wind_deg'],  # degrees
            'weather': response["current"]['weather'][0]['main']}


# Calculate the points lat and long by distance and degree
def cal_point(lat, lon, length, degree):
    start_point = Point(lat, lon)
    des_point = distance(kilometers=length).destination(point=start_point, bearing=degree)
    return [des_point.latitude, des_point.longitude]


def get_locations(request):
    # Get the current weather information
    weather_info = get_weather_cur()
    # Get the ryegrass locations data
    now = timezone.now()
    check_date = now - relativedelta(years=3)
    ryegrass = Ryegrass.objects.filter(
        Q(rye_date__gte=check_date)
    ).values()
    ryegrass = list(ryegrass)
    # Get the shape points of the risk areas
    results = []
    for data in ryegrass:
        # Get the center of the risk area
        center_lat = data['rye_lat']
        center_lon = data['rye_lon']
        # Get the wind_deg
        wind_deg = weather_info['wind_deg']
        # Sign the value of radius and extend_length
        radius = 0.5  # km the radius of the risk area
        extend_length = 1.5  # km the length of the wind direction
        # Calculate the shape points
        shape_points = ['M', cal_point(center_lat, center_lon, radius, wind_deg + 90),
                        'Q', cal_point(center_lat, center_lon, radius * sqrt(2), wind_deg + 45),
                        cal_point(center_lat, center_lon, radius, wind_deg),
                        'T', cal_point(center_lat, center_lon, radius, wind_deg - 90),
                        'L', cal_point(center_lat, center_lon, extend_length, wind_deg - 150),
                        'Q', cal_point(center_lat, center_lon, extend_length, wind_deg - 165),
                        cal_point(center_lat, center_lon, extend_length, wind_deg - 180),
                        'Q', cal_point(center_lat, center_lon, extend_length, wind_deg - 195),
                        cal_point(center_lat, center_lon, extend_length, wind_deg - 210),
                        'Z']
        # Get the current month and current weather
        weather = weather_info['weather']
        month = now.month
        pollen_months = [9, 10, 11, 12, 1, 2]
        # Get the shape color
        if month in pollen_months:
            if weather == 'Rain':
                shape_color = 'yellow'
                popup_message = 'The risk of Ryegrass pollen become lower due to the rain.'
            else:
                shape_color = 'red'
                popup_message = 'The risk of Ryegrass pollen is high.'
        else:
            shape_color = 'green'
            popup_message = 'The risk of Ryegrass pollen is low, feel free to go outside.'
        # Generate the result
        result = {'month': month,
                  'shape_points': shape_points,
                  'weather': weather,
                  'shape_color': shape_color,
                  'popup_message': popup_message,
                  'rye_name': data['rye_vernacular_name']}
        # Append the result to the results
        results.append(result)
    # Return the results
    return JsonResponse(results, safe=False)


def get_danger_areas(request):
    weather_info = get_weather_cur()
    # Get the ryegrass locations data
    now = timezone.now()
    check_date = now - relativedelta(years=3)
    ryegrass = Ryegrass.objects.filter(
        Q(rye_date__gte=check_date)
    ).values()
    ryegrass = list(ryegrass)
    # Get the shape points of the risk areas
    results = []
    for data in ryegrass:
        # Get the center of the risk area
        center_lat = data['rye_lat']
        center_lon = data['rye_lon']
        # Get the wind_deg
        wind_deg = weather_info['wind_deg']
        # Sign the value of radius and extend_length
        radius = 0.5  # km the radius of the risk area
        extend_length = 1.5  # km the length of the wind direction
        # Calculate the shape points
        danger_area = [cal_point(center_lat, center_lon, radius, wind_deg - 90),
                       cal_point(center_lat, center_lon, radius * sqrt(2), wind_deg - 135),
                       cal_point(center_lat, center_lon, radius, wind_deg - 180),
                       cal_point(center_lat, center_lon, radius * sqrt(2), wind_deg - 225),
                       cal_point(center_lat, center_lon, radius, wind_deg - 270),
                       cal_point(center_lat, center_lon, extend_length, wind_deg)]
        # Get the current month and current weather
        weather = weather_info['weather']
        month = now.month
        pollen_months = [9, 10, 11, 12, 1, 2]
        # Get the shape color
        if month in pollen_months:
            if weather == 'Rain':
                risk = 'mid'  # yellow
            else:
                risk = 'high'
        else:
            risk = 'low'
        # Generate the result
        result = {'danger_area': danger_area,
                  'risk': risk}
        # Append the result to the results
        results.append(result)
    # Return the results
    return JsonResponse(results, safe=False)


def cloth_edu(request):
    if request.session.get('is_logged_in'):
        # print(request.session.get('is_logged_in'))
        return render(request, 'Cloth_Edu.html')
    else:
        return redirect('login')


def base(request):
    return render(request, 'base.html')


def allergy_hub(request):
    # symptoms = Symptom.objects.all()
    # sample_rate_data = calculate_percentage()
    # sample_rate_data_json = json.dumps(sample_rate_data)
    # return render(request, 'Allergy_Hub.html', {'symptoms': symptoms, 'sampleRateData': sample_rate_data_json})
    if request.session.get('is_logged_in'):
        symptoms = Symptom.objects.all()
        sample_rate_data = calculate_percentage()
        sample_rate_data_json = json.dumps(sample_rate_data)
        return render(request, 'Allergy_Hub.html', {
            'symptoms': symptoms,
            'sampleRateData': sample_rate_data_json
        })
    else:
        return redirect('login')


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


def cloth_sug(request):
    # Check if the user is already logged in
    if not request.session.get('is_logged_in'):
        return redirect('login')  # If user is not logged in, redirect to login page

    if request.method == 'POST':
        form = ExposureTimeForm(request.POST)
        if form.is_valid():
            # The form data is valid and suggestions are generated
            suggestions = generate_suggestions(form.cleaned_data['duration'])
            return render(request, 'cloth_view.html', {'suggestions': suggestions})
    else:
        # Not a POST request, just showing an empty form
        form = ExposureTimeForm()

    return render(request, 'cloth_view.html', {'form': form})


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
        # return redirect('Allergy_Hub.html')
        if request.session.get('is_logged_in'):
            return render(request, 'Allergy_Hub.html')
        else:
            return redirect('login')
