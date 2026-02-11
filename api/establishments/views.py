from .models import Establishment
from .serializers import EstablishmentSerializer


def establishments_list(request):
    establishments = Establishment.objects.all()
    return EstablishmentSerializer(establishments).json_response()
