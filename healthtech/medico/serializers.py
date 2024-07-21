from rest_framework import serializers

class MedicoAgendaSerializer(serializers.Serializer):
    data_inicio = serializers.DateTimeField()
    data_fim = serializers.DateTimeField(required=False)
    valor = serializers.FloatField(required=False)