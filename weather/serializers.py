from rest_framework import serializers
from .models import WeatherData, Location

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["id", "name", "lon", "lat"]

class WeatherSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)  # nested serializer for location

    class Meta:
        model = WeatherData
        fields = [
            "id",
            "temperature",
            "humidity",
            "wind",
            "pressure",
            "description",
            "timestamp",
            "location",
        ]