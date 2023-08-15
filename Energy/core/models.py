from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Casa(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    valores_kwh = models.JSONField(default=list)  
    valores_pagar = models.JSONField(default=list)
    areaCuadrada = models.FloatField()
    dispositivos = models.ManyToManyField('Dispositivos', related_name='dispositivos')

    def __str__(self):
        return self.name

class Dispositivos(models.Model):
    casa = models.ForeignKey('Casa', related_name='devices', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    consumoWPerH = models.FloatField()
    horasActivo = models.FloatField()
    
    def __str__(self):
        return self.name

    

class Metas(models.Model):
    casa = models.ForeignKey(Casa, related_name='goals', on_delete=models.CASCADE)
    description = models.TextField()
    
    def __str__(self):
        return self.description