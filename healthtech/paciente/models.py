from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class PerfilPaciente(models.Model):
    uuid = models.UUIDField(primary_key=True)
    nome = models.CharField(max_length=120, blank=False)
    email = models.EmailField(blank=False)
    cpf = models.CharField(max_length=11, blank=False, null=False)
    