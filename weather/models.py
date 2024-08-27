from decimal import Decimal as D
import pytz

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

from services.utils import convert_celsius_to_fahreheit, convert_kmph_to_mph


class WindDirectionChoices(models.TextChoices):
    N = "N", _("North")
    S = "S", _("South")
    E = "E", _("East")
    W = "W", _("West")
    NE = "NE", _("Northeast")
    SE = "SE", _("Southeast")
    SW = "SW", _("Southwest")
    NW = "NW", _("Northwest")


class LocationWeather(models.Model):
    name = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    condition = models.CharField(max_length=300, blank=True)
    condition_icon = models.URLField(blank=True)
    temperature = models.DecimalField(
        max_digits=5, decimal_places=2, 
        help_text="Temperature in Celsius", 
        validators=[MinValueValidator(D('-100')), MaxValueValidator(D('60'))]
    )
    temperature_feels_like = models.DecimalField(
        max_digits=5, decimal_places=2, 
        help_text="Temperature in Celsius", 
        validators=[MinValueValidator(D('-100')), MaxValueValidator(D('60'))]
    )
    wind_speed = models.DecimalField(
        max_digits=5, decimal_places=2, 
        help_text="Wind speed in kilometers per hour", 
        validators=[MinValueValidator(D('0'))]
    )
    wind_direction = models.CharField(choices=WindDirectionChoices.choices, max_length=2)
    pressure = models.DecimalField(
        max_digits=6, decimal_places=2, 
        help_text="Pressure in millibars", 
        validators=[MinValueValidator(D('870')), MaxValueValidator(D('1080'))]
    )
    precipitation = models.DecimalField(
        max_digits=5, decimal_places=2, 
        help_text="Precipitation in millimeters", 
        validators=[MinValueValidator(D('0'))]
    )
    humidity = models.DecimalField(
        max_digits=5, decimal_places=2, 
        help_text="Humidity percentage", 
        validators=[MinValueValidator(D('0')), MaxValueValidator(D('100'))]
    )
    dewpoint = models.DecimalField(
        max_digits=5, decimal_places=2, 
        help_text="Dewpoint in Celsius",
        validators=[MinValueValidator(D('-100')), MaxValueValidator(D('60'))]
    )
    uv_index = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(11)]
    )
    gust_speed = models.DecimalField(
        max_digits=5, decimal_places=2, 
        help_text="Gust in kilometers per hour", 
        validators=[MinValueValidator(D('0'))]
    )
    visibility = models.DecimalField(
        max_digits=5, decimal_places=2, 
        help_text="Visibility in kilometers", 
        validators=[MinValueValidator(D('0'))]
    )

    record_timestamp = models.DateTimeField(help_text="Time in UTC")
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["name", "-record_timestamp"])]

    @property
    def temperature_in_fahrenheit(self):
        return round(convert_celsius_to_fahreheit(float(self.temperature)), 2)

    @property
    def wind_speed_in_mph(self):
        """Wind speed in mile per hour"""
        return round(convert_kmph_to_mph(float(self.wind_speed)), 2)

    @property
    def record_time_to_asia_kolkata(self):
        kolkata_tz = pytz.timezone('Asia/Kolkata')
        return self.record_timestamp.astimezone(kolkata_tz).time()

    def __str__(self):
        return f"{self.name} ({self.record_timestamp.strftime('%Y-%m-%d %H:%M:%S')})"
