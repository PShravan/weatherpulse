from dataclasses import asdict
from datetime import datetime

from services.weatherapi import get_weather_data_via_api, LocationWeatherData
from weather.models import LocationWeather


def create_locationweater_entry(
    *,
    name: str,
    region: str,
    country: str,
    latitude,
    longitude,
    condition,
    condition_icon,
    temperature,
    temperature_feels_like,
    wind_speed,
    wind_direction,
    pressure,
    precipitation,
    humidity,
    dewpoint,
    uv_index,
    gust_speed,
    visibility,
    record_timestamp: datetime,
) -> LocationWeather:
    """Create a new weather entry for a specific location."""
    return LocationWeather.objects.create(
        name=name.lower(),
        region=region,
        country=country,
        latitude=latitude,
        longitude=longitude,
        condition=condition,
        condition_icon=condition_icon,
        temperature=temperature,
        temperature_feels_like=temperature_feels_like,
        wind_speed=wind_speed,
        wind_direction=wind_direction,
        pressure=pressure,
        precipitation=precipitation,
        humidity=humidity,
        dewpoint=dewpoint,
        uv_index=uv_index,
        gust_speed=gust_speed,
        visibility=visibility,
        record_timestamp=record_timestamp,
    )



def fetch_location_current_weather(name) -> LocationWeather:
    weather_data: LocationWeatherData = get_weather_data_via_api(location=name)
    return create_locationweater_entry(**asdict(weather_data))
