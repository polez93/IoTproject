from django import forms
from .models import Cliente, Granja, Instalacion,Sensor,Lectura

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'telefono' , 'correo']
        widgets = {
            'nombre' : forms.TextInput(attrs={'class':'form-control','placeholder': 'Ingrese Nombre'}),
            'telefono' : forms.TextInput(attrs={'class':'form-control','placeholder':'Numero celular'}),
            'correo' : forms.TextInput(attrs={'class':'form-control','placeholder':'correo electronico'})
        }
  
class GranjaForm(forms.ModelForm):
    class Meta:
        model = Granja
        fields = ['nombre', 'ubicacion']
        widgets = {
            'nombre' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre de la granja'}),
            'ubicacion': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Ubicación de la granja'})
        }

class InstalacionForm(forms.ModelForm):
    class Meta:
        model = Instalacion
        fields = ['referencia', 'descripcion', 'ubicacion','granja']
        widgets = {
            'referencia' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Referencia'}),
            'descripcion' : forms.Textarea(attrs={'class':'form-control','style':'height: 20vh;', 'placeholder':'descripcion'}),
            'ubicacion' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ubicacion'}),
            'granja' : forms.Select(attrs={'class':'form-control'})
        }
    
    def __init__(self, *args, **kwargs):
        cliente = kwargs.pop('cliente', None)
        super(InstalacionForm, self).__init__(*args, **kwargs)
        if cliente:
            self.fields['granja'].queryset = Granja.objects.filter(cliente=cliente)

class SensorForm(forms.ModelForm):
    class Meta:
        model = Sensor
        fields = ['nombre','parametro','maxValor','minValor','ubicacion','instalacion']
        widgets = {
            'nombre' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre'}),
            'parametro' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Parametro'}),
            'maxValor' : forms.NumberInput(attrs={'class':'form-control'}),
            'minValor' : forms.NumberInput(attrs={'class':'form-control'}),
            'ubicacion' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ubicación'}),
            'instalacion' : forms.Select(attrs={'class':'form-control'})
        }
    def __init__(self, *args, **kwargs):
        cliente = kwargs.pop('cliente', None)
        super(SensorForm, self).__init__(*args, **kwargs)
        if cliente:
            self.fields['instalacion'].queryset = Instalacion.objects.filter(granja__cliente=cliente)
