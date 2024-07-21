from django.db import models
import uuid
# Create your models here.


class Agenda(models.Model):
    status_choice = [
        ('disponivel', 'disponivel'),
        ('aguardando_confirmacao', 'aguardando_confirmacao'),
        ('confirmada', 'confirmada'),
        ('realizada', 'realizada'),
        ('cancelada', 'cancelada'),
    ]
    uuid = models.UUIDField(primary_key=True ,default=uuid.uuid4, editable=False)
    uuid_medico = models.UUIDField(blank=False)
    nome_medico = models.CharField(max_length=120, blank=False)
    especialidade = models.CharField(max_length=40, blank=False)
    uuid_paciente = models.CharField(max_length=120, blank=True)
    nome_paciente = models.CharField(max_length=120, blank=True)
    data_inicio = models.DateTimeField(blank=False)
    data_fim = models.DateTimeField(blank=False)
    valor_consulta = models.FloatField(null=False)
    status = models.CharField(choices=status_choice,
                              default='disponivel', max_length=40)
