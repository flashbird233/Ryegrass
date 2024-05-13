# Remove the records of ryegrass from the database
import os

import django
from django.http import JsonResponse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ryegrass.settings')
django.setup()

import requests
from dateutil.relativedelta import relativedelta
from django.db.models import Q
from django.utils import timezone
from geopy import Point
from geopy.distance import distance

from Breathe_Ease_Home.models import Ryegrass


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


# Get the shape points of risk areas
def get_locations(weather_info):
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
        shape_points = ['M', cal_point(center_lat, center_lon, radius, wind_deg - 90),
                        'Q', cal_point(center_lat, center_lon, radius, wind_deg - 135),
                        cal_point(center_lat, center_lon, radius, wind_deg - 180),
                        'T', cal_point(center_lat, center_lon, radius, wind_deg - 270),
                        'L', cal_point(center_lat, center_lon, extend_length, wind_deg),
                        'Z']
        # Get the current month and current weather
        weather = weather_info['weather']
        month = now.month
        pollen_months = [9, 10, 11, 12, 1, 2]
        # Get the shape color
        if month in pollen_months:
            if weather == 'Rain':
                color = 'yellow'  # yellow
            else:
                color = 'red'
        else:
            color = 'green'
        # Generate the result
        result = {'month': month,
                  'shape_points': shape_points,
                  'weather': weather,
                  'color': color}
        # Append the result to the results
        results.append(result)
    # Return the results
    return results


def get_locations2(request):
    # Only keep last 3 years data
    now = timezone.now()
    check_date = now - relativedelta(years=3)
    ryegrass = Ryegrass.objects.filter(
        Q(rye_date__gte=check_date)
    ).values()

    return JsonResponse(list(ryegrass), safe=False)


def test_get_locations2():
    from django.test import RequestFactory
    request = RequestFactory().get('/')
    response = get_locations2(request)
    print(response.content)


a = get_locations(get_weather_cur())
print(a)
b = test_get_locations2()
print(b)
