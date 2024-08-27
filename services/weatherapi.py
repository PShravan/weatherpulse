import logging
import requests
from dataclasses import dataclass
from datetime import datetime

from django.conf import settings

from services.utils import convert_ist_to_utc


logger = logging.getLogger(__name__)


class NoLocationFoundException(Exception):
    """No location found for the given query"""


@dataclass
class LocationWeatherData:
    name: str
    region: str
    country: str
    latitude: float
    longitude: float
    condition: str
    condition_icon: str
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
        current_condition = weather_data.get("condition", {})
        record_timestamp = convert_ist_to_utc(weather_data["last_updated"])
        return LocationWeatherData(
            name=location_data["name"],
            region=location_data["region"],
            country=location_data["country"],
            latitude=location_data["lat"],
            longitude=location_data["lon"],
            condition=current_condition.get("text", ""),
            condition_icon=current_condition.get("icon", ""),
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
    if response.status_code == 400 and response_json["error"]["code"] == 1006:
        raise NoLocationFoundException("No Location Found!")
    logger.error(f"WeatherAPI failure! StatusCode: {response.status_code}, Error:{response_json.get('error')}")
    raise Exception(f"Something went wrong!")


def get_weather_forecast_data_via_api(location: str, days=1):
    """
    response:
    status_code: 200
    json: {
        "location": {
            "name": "New York",
            "region": "New York",
            "country": "United States of America",
            "lat": 40.71,
            "lon": -74.01,
            "tz_id": "America/New_York",
            "localtime_epoch": 1658522976,
            "localtime": "2022-07-22 16:49"
        },
        "current": {
            "last_updated_epoch": 1658522700,
            "last_updated": "2022-07-22 16:45",
            "temp_c": 34.4,
            "temp_f": 93.9,
            "is_day": 1,
            "condition": {
            "text": "Partly cloudy",
            "icon": "//cdn.weatherapi.com/weather/64x64/day/116.png",
            "code": 1003
            },
            "wind_mph": 16.1,
            "wind_kph": 25.9,
            "wind_degree": 180,
            "wind_dir": "S",
            "pressure_mb": 1011,
            "pressure_in": 29.85,
            "precip_mm": 0,
            "precip_in": 0,
            "humidity": 31,
            "cloud": 75,
            "feelslike_c": 37,
            "feelslike_f": 98.6,
            "vis_km": 16,
            "vis_miles": 9,
            "uv": 8,
            "gust_mph": 11.6,
            "gust_kph": 18.7,
            "air_quality": {
            "co": 293.70001220703125,
            "no2": 18.5,
            "o3": 234.60000610351562,
            "so2": 12,
            "pm2_5": 13.600000381469727,
            "pm10": 15,
            "us-epa-index": 1,
            "gb-defra-index": 2
            }
        },
        "forecast": {
            "forecastday": [
            {
                "date": "2022-07-22",
                "date_epoch": 1658448000,
                "day": {
                "maxtemp_c": 35.9,
                "maxtemp_f": 96.6,
                "mintemp_c": 26.3,
                "mintemp_f": 79.3,
                "avgtemp_c": 30.7,
                "avgtemp_f": 87.3,
                "maxwind_mph": 12.8,
                "maxwind_kph": 20.5,
                "totalprecip_mm": 0,
                "totalprecip_in": 0,
                "avgvis_km": 10,
                "avgvis_miles": 6,
                "avghumidity": 53,
                "daily_will_it_rain": 0,
                "daily_chance_of_rain": 0,
                "daily_will_it_snow": 0,
                "daily_chance_of_snow": 0,
                "condition": {
                    "text": "Sunny",
                    "icon": "//cdn.weatherapi.com/weather/64x64/day/113.png",
                    "code": 1000
                },
                "uv": 8
                },
                "astro": {
                "sunrise": "05:44 AM",
                "sunset": "08:20 PM",
                "moonrise": "12:58 AM",
                "moonset": "03:35 PM",
                "moon_phase": "Last Quarter",
                "moon_illumination": "36"
                },
                "hour": [
                {
                    "time_epoch": 1658462400,
                    "time": "2022-07-22 00:00",
                    "temp_c": 28.7,
                    "temp_f": 83.7,
                    "is_day": 0,
                    "condition": {
                    "text": "Clear",
                    "icon": "//cdn.weatherapi.com/weather/64x64/night/113.png",
                    "code": 1000
                    },
                    "wind_mph": 9.4,
                    "wind_kph": 15.1,
                    "wind_degree": 265,
                    "wind_dir": "W",
                    "pressure_mb": 1007,
                    "pressure_in": 29.73,
                    "precip_mm": 0,
                    "precip_in": 0,
                    "humidity": 58,
                    "cloud": 19,
                    "feelslike_c": 30.5,
                    "feelslike_f": 86.9,
                    "windchill_c": 28.7,
                    "windchill_f": 83.7,
                    "heatindex_c": 30.5,
                    "heatindex_f": 86.9,
                    "dewpoint_c": 19.6,
                    "dewpoint_f": 67.3,
                    "will_it_rain": 0,
                    "chance_of_rain": 0,
                    "will_it_snow": 0,
                    "chance_of_snow": 0,
                    "vis_km": 10,
                    "vis_miles": 6,
                    "gust_mph": 15,
                    "gust_kph": 24.1,
                    "uv": 1
                }
                ]
            }
            ]
        },
        "alerts": {
            "alert": [
            {
                "headline": "NWS New York City - Upton (Long Island and New York City)",
                "msgtype": null,
                "severity": null,
                "urgency": null,
                "areas": null,
                "category": "Extreme temperature value",
                "certainty": null,
                "event": "Heat Advisory",
                "note": null,
                "effective": "2022-07-21T19:38:00+00:00",
                "expires": "2022-07-25T00:00:00+00:00",
                "desc": "...HEAT ADVISORY REMAINS IN EFFECT UNTIL 8 PM EDT SUNDAY... * WHAT...Heat index values up to 105. * WHERE...Eastern Passaic Hudson Western Bergen Western Essex Eastern Bergen and Eastern Essex Counties. * WHEN...Until 8 PM EDT Sunday. * IMPACTS...High temperatures and high humidity may cause heat illnesses to occur.",
                "instruction": ""
            }
            ]
        }
    }

    invalid location:
    {
        "code": 1006,
        "message": "No location found matching parameter 'q'"
    }
    """

    url = f"http://api.weatherapi.com/v1/forecast.json?key={settings.WEATHERAPI_API_KEY}&q={location}&days={days}"
    response = requests.get(url)
    response_json = response.json()
    if response.status_code == 200:
        location_data = response_json["location"]
        weather_data = response_json["current"]
        current_condition = weather_data.get("condition", {})
        record_timestamp = convert_ist_to_utc(weather_data["last_updated"])
        return LocationWeatherData(
            name=location_data["name"],
            region=location_data["region"],
            country=location_data["country"],
            latitude=location_data["lat"],
            longitude=location_data["lon"],
            condition=current_condition.get("text", ""),
            condition_icon=current_condition.get("icon", ""),
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
    if response.status_code == 400 and response_json["error"]["code"] == 1006:
        raise NoLocationFoundException("No Location Found!")
    logger.error(f"WeatherAPI failure! StatusCode: {response.status_code}, Error:{response_json.get('error')}")
    raise Exception(f"Something went wrong!")
