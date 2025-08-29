import os

from celery import shared_task
import requests
from django.utils import timezone
from .models import Location, WeatherData
from dotenv import load_dotenv

@shared_task
def fetch_weather_data():
    # Example: loop through all stored locations
    for location in Location.objects.all():
        try:
            # Replace with your actual API call
            url = ("http://api.openweathermap.org/data/2.5/weather?q=Milan,it" + "&" +
                   "APPID=" + os.getenv('WEATHER_API_KEY') +  "units=metri")

            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            current = data.get("current_weather", {})

            # Save to DB

            WeatherData.objects.create(
                temperature=current.get("temperature"),
                humidity=current.get("relativehumidity", 0),  # adjust based on API fields
                wind=current.get("windspeed", 0),
                pressure=current.get("pressure", 0),
                description="Weather update",
                timestamp=timezone.now(),
                location=location,
            )


        except Exception as e:
            # Log or retry as needed
            print(f"Error fetching weather for {location.name}: {e}")