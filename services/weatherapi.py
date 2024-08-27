import requests
from dataclasses import dataclass
from datetime import datetime

from django.conf import settings

from services.utils import convert_ist_to_utc


class NoLocationFoundException(Exception):
    """No location found for the given query"""


@dataclass
class LocationWeatherData:
    name: str
    region: str
    country: str
    latitude: float
    longitude: float
    temperature: float
    temperature_feels_like: float
    wind_speed: float
    wind_direction: str
    pressure: float
    precipitation: float
    humidity: float
    dewpoint: float
    uv_index: int
    gust_speed: float
    visibility: float
    record_timestamp: datetime


def get_weather_data_via_api(location: str):
    """
    response:
    status_code: 200
    json: {
        "location": {
            "name": "Warangal",
            "region": "Andhra Pradesh",
            "country": "India",
            "lat": 18,
            "lon": 79.58,
            "tz_id": "Asia/Kolkata",
            "localtime_epoch": 1725708104,
            "localtime": "2024-09-07 16:51"
        },
        "current": {
            "last_updated_epoch": 1725707700,
            "last_updated": "2024-09-07 16:45",
            "temp_c": 29.1,
            "temp_f": 84.4,
            "is_day": 1,
            "condition": {
                "text": "Patchy rain nearby",
                "icon": "//cdn.weatherapi.com/weather/64x64/day/176.png",
                "code": 1063
            },
            "wind_mph": 9.8,
            "wind_kph": 15.8,
            "wind_degree": 308,
            "wind_dir": "NW",
            "pressure_mb": 1003,
            "pressure_in": 29.61,
            "precip_mm": 0.53,
            "precip_in": 0.02,
            "humidity": 75,
            "cloud": 74,
            "feelslike_c": 33.9,
            "feelslike_f": 93,
            "windchill_c": 29.1,
            "windchill_f": 84.4,
            "heatindex_c": 33.9,
            "heatindex_f": 93,
            "dewpoint_c": 24.2,
            "dewpoint_f": 75.6,
            "vis_km": 9,
            "vis_miles": 5,
            "uv": 6,
            "gust_mph": 13.4,
            "gust_kph": 21.6
        }
    }

    invalid location:
    {
        "code": 1006,
        "message": "No location found matching parameter 'q'"
    }
    """

    url = f"http://api.weatherapi.com/v1/current.json?key={settings.WEATHERAPI_API_KEY}&q={location}"
    response = requests.get(url)
    response_json = response.json()
    if response.status_code == 200:
        location_data = response_json["location"]
        weather_data = response_json["current"]
        record_timestamp = convert_ist_to_utc(weather_data["last_updated"])
        return LocationWeatherData(
            name=location_data["name"],
            region=location_data["region"],
            country=location_data["country"],
            latitude=location_data["lat"],
            longitude=location_data["lon"],
            temperature=weather_data["temp_c"],
            temperature_feels_like=weather_data["feelslike_c"],
            wind_speed=weather_data["wind_kph"],
            wind_direction=weather_data["wind_dir"],
            pressure=weather_data["pressure_mb"],
            precipitation=weather_data["precip_mm"],
            humidity=weather_data["humidity"],
            dewpoint=weather_data["dewpoint_c"],
            uv_index=weather_data["uv"],
            gust_speed=weather_data["gust_kph"],
            visibility=weather_data["vis_km"],
            record_timestamp=record_timestamp,
        )
    # TODO: add logging
    if response.status_code == 400 and response_json["error"]["code"] == 1006:
        raise NoLocationFoundException("No Location Found!")
    raise Exception(f"Something went wrong!")
