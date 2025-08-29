from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import WeatherData
from .serializers import WeatherSerializer

# Create your views here.

@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def WeatherViewSet(request):
    qs = WeatherData.objects.last()
    serializer = WeatherSerializer(qs)
    return Response(serializer.data)
