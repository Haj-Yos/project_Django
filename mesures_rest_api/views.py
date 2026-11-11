from django.utils.dateparse import parse_datetime

from rest_framework.generics import ListAPIView

from grandeurs.models import Mesure
from .serializers import MesureSerializer


class MesureListAPIView(ListAPIView):

    serializer_class = MesureSerializer

    def get_queryset(self):
        grandeur_id = self.request.query_params.get('grandeur')

        start = self.request.query_params.get('start')
        end = self.request.query_params.get('end')

        queryset = Mesure.objects.select_related('grandeur')

        if grandeur_id:
            queryset = queryset.filter(
                grandeur_id=grandeur_id
            )

        if start and end:
            start_dt = parse_datetime(start)
            end_dt = parse_datetime(end)

            queryset = queryset.filter(
                datePrise__range=[start_dt, end_dt]
            )

        return queryset.order_by('datePrise')