from django.shortcuts import render

from services.weatherapi import NoLocationFoundException
from weather.forms import LocationSearchForm
from weather.services import fetch_location_current_weather
from weather.selectors import get_weather_alert, get_weather_trends


def home(request):
    location = 'warangal' # default location
    weather_alert = None
    weather_trends = None
    latest_weather = None
    error_message = None
    form = LocationSearchForm()

    if request.method == 'POST':
        form = LocationSearchForm(request.POST)
        if form.is_valid():
            location = form.cleaned_data['location'].lower()
    try:
        # Fetch the latest weather and check alerts
        latest_weather = fetch_location_current_weather(location)
        weather_alert = get_weather_alert(latest_weather)
        # Fetch trends over the last 24 hours
        weather_trends = get_weather_trends(location, days=1)
    except NoLocationFoundException:
        error_message = "No Location Found!"

    context = {
        'form': form,
        'location': location,
        'latest_weather': latest_weather,
        'weather_alert': weather_alert,
        'weather_trends': weather_trends,
        'error_message': error_message,
    }
    
    return render(request, 'weather/home.html', context)
