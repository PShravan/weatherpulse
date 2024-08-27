from django.utils.timezone import now, timedelta
from django.db import models

from weather.models import LocationWeather


def get_latest_weather_for_location(name):
    """Fetch the latest weather data for a given location by name."""
    return LocationWeather.objects.filter(name=name).order_by('-record_timestamp').first()


def get_weather_trends(name, days=1):
    """Calculate average weather trends (e.g., temperature, humidity) over the last 'days' days."""
    end_time = now()
    start_time = end_time - timedelta(days=days)
    
    weather_data = LocationWeather.objects.filter(
        name=name,
        record_timestamp__range=[start_time, end_time]
    )

    if weather_data.exists():
        avg_temp = weather_data.aggregate(models.Avg('temperature'))['temperature__avg']
        avg_wind = weather_data.aggregate(models.Avg('wind_speed'))['wind_speed__avg']
        avg_pressure = weather_data.aggregate(models.Avg('pressure'))['pressure__avg']
        avg_precipitation = weather_data.aggregate(models.Avg('precipitation'))['precipitation__avg']
        avg_humidity = weather_data.aggregate(models.Avg('humidity'))['humidity__avg']
        avg_dewpoint = weather_data.aggregate(models.Avg('dewpoint'))['dewpoint__avg']
        return {
            'average_temperature': round(avg_temp, 2),
            'average_wind': round(avg_wind, 2),
            'average_pressure': round(avg_pressure, 2),
            'average_precipitation': round(avg_precipitation, 2),
            'average_humidity': round(avg_humidity, 2),
            'average_dewpoint': round(avg_dewpoint, 2),
        }
    return None


def check_for_extreme_conditions(weather_data):
    """Check if the current weather data contains extreme conditions."""
    extreme_conditions = []
    
    if weather_data.temperature > 35 or weather_data.temperature < 0:
        extreme_conditions.append('Extreme temperature')
    if weather_data.wind_speed > 100:
        extreme_conditions.append('High wind speed')
    if weather_data.humidity > 90:
        extreme_conditions.append('High humidity')
    if weather_data.pressure < 980 or weather_data.pressure > 1050:
        extreme_conditions.append('Extreme pressure')

    return extreme_conditions if extreme_conditions else None


def get_weather_alert(weather_data: LocationWeather):
    """return any alerts for extreme conditions."""
    if weather_data:
        extreme_conditions = check_for_extreme_conditions(weather_data)
        if extreme_conditions:
            return f"Alert: {', '.join(extreme_conditions)}"
    return None
