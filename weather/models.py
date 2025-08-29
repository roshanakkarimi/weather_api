from django.db import models

# Create your models here.

class Location(models.Model):
    name = models.CharField(max_length=100)
    lon = models.FloatField()
    lat = models.FloatField()

    def __str__(self):
        return self.name


class WeatherData(models.Model):
    temperature = models.FloatField()
    humidity = models.FloatField()
    wind = models.FloatField()
    pressure = models.FloatField()
    description = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="weather_data")

    def __str__(self):
        return f"{self.description} @ {self.location.name} ({self.timestamp})"


class WeatherAlert(models.Model):
    window = models.ManyToManyField(WeatherData, related_name="alerts")
    speed = models.IntegerField(default=0)
