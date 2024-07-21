from django.db import models

# Create your models here.
class PerfilMedico(models.Model):
    uuid = models.UUIDField(primary_key=True)
    nome = models.CharField(max_length=120, blank=False)
    email = models.EmailField(blank=False)
    crm = models.CharField(max_length=8, blank=False, null=False)
    especialidade = models.CharField(max_length=40, blank=False)
    valor_consulta = models.FloatField(null=False)
