
from rest_framework import serializers
from grandeurs.models import Mesure

class MesureSerializer(serializers.ModelSerializer):

    grandeur_nom = serializers.CharField(
        source="grandeur.nom",
        read_only=True
    )

    unite = serializers.CharField(
        source="grandeur.unite",
        read_only=True
    )

    class Meta:
        model = Mesure

        fields = [
            'id',
            'valeur',
            'datePrise',
            'grandeur',
            'grandeur_nom',
            'unite'
        ]