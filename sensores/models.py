from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class Cliente(models.Model):
    nombre = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20)
    correo = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')

    def __str__(self):
        return self.nombre

class Granja(models.Model):
    nombre = models.CharField(max_length=30)
    ubicacion = models.TextField(max_length=100)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='granjas')
    def __str__(self):
        return self.nombre

class Instalacion(models.Model):
    referencia = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=200)
    ubicacion = models.TextField(max_length=100)
    granja = models.ForeignKey(Granja, on_delete=models.CASCADE, related_name='instalaciones')
    def __str__(self):
        return self.referencia

class Sensor(models.Model):
    nombre = models.CharField(max_length=50)
    parametro = models.CharField(max_length=30)
    maxValor = models.DecimalField(max_digits=8, decimal_places=2)
    minValor = models.DecimalField(max_digits=8, decimal_places=2)
    ubicacion = models.TextField(max_length=100)
    active = models.BooleanField(default=True)
    instalacion = models.ForeignKey(Instalacion, on_delete=models.CASCADE, related_name='sensores')
    
    def __str__(self):
        return self.nombre

class Lectura(models.Model):
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(default=datetime.now())
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='lecturas')
    def __str__(self):
        return self.valor + self.hora.strftime('%H:%M:%S')
