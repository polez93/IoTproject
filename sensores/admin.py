from django.contrib import admin
from .models import Cliente, Granja, Instalacion, Sensor

# Register your models here.
class SensorInline(admin.TabularInline):
    model = Sensor
    extra = 1

class InstalacionInline(admin.TabularInline):
    model = Instalacion
    extra = 1
    inlines = [SensorInline]

class GranjaInline(admin.TabularInline):
    model = Granja
    extra = 1
    inlines = [InstalacionInline]

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    inlines = [GranjaInline]
    list_display = ('id','nombre', 'user')

@admin.register(Granja)
class GranjaAdmin(admin.ModelAdmin):
    inlines = [InstalacionInline]
    list_display = ('id','nombre', 'cliente')

@admin.register(Instalacion)
class InstalacionAdmin(admin.ModelAdmin):
    inlines = [SensorInline]
    list_display = ('id','referencia', 'granja')

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ('id','nombre', 'instalacion')
    search_fields = ('nombre',)