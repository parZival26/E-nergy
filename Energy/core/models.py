from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator


User = get_user_model()

class Casa(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='Nombre de la casa')
    valores_kwh = models.JSONField(default=list)  
    valores_pagar = models.JSONField(default=list)
    areaCuadrada = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.0)], verbose_name="Area cuadrada de la casa")
    dispositivos = models.ManyToManyField('Dispositivos', related_name='dispositivos')

    def __str__(self):
        return self.name

class Dispositivos(models.Model):
    casa = models.ForeignKey('Casa', related_name='devices', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="Nombre del dispositivo")
    consumoWPerH = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.0)], verbose_name="Consumo en Watts por hora")
    horasActivo = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.0)], verbose_name="Horas activo por dia")
    
    def __str__(self):
        return self.name

    

class Metas(models.Model):
    casa = models.ForeignKey(Casa, related_name='goals', on_delete=models.CASCADE)
    description = models.TextField(verbose_name="Descripcion de la meta")
    
    def __str__(self):
        return self.description