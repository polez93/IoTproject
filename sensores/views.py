from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import JsonResponse
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.axes import XValueAxis, YValueAxis
from reportlab.graphics.shapes import Drawing
import io
import datetime

from django.contrib.auth.decorators import login_required
from .forms import ClienteForm, GranjaForm, InstalacionForm, SensorForm
from .models import Cliente, Granja, Instalacion, Sensor, Lectura

# Create your views here.


def home(request):
    return render(request, 'home.html')

def generate_pdf(request, sensor_id):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="lecturas.pdf"'

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    lecturas = Lectura.objects.filter(sensor=sensor_id)
    data = [['Sensor', 'Fecha','Hora','Valor']]
    valores = []
    fechas = []
    for lectura in lecturas:
        data.append([lectura.sensor, lectura.fecha, lectura.hora, str(lectura.valor)])
        valores.append(float(lectura.valor))
        fechas.append(lectura.hora)
    #crear tabla
    col_widths = [150, 150, 100]
    table = Table(data, colWidths=col_widths)
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.bisque),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BOX', (0, 0), (-1, -1), 2, colors.black),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('ROUNDRECT', (0, 0), (-1, -1), 20, 20),
    ])
    table.setStyle(style)

    #crear gráfico
    drawing = Drawing(400, 200)
    line = LinePlot()
    line.x = 50
    line.y = 50
    line.width = 300
    line.height = 125
    line.data = [list(zip(range(len(fechas)), valores))]
    line.lines[0].strokeColor = colors.blue

    # Configurar ejes
    line.xValueAxis = XValueAxis()
    line.xValueAxis.valueMin = 0
    line.xValueAxis.valueMax = len(fechas) - 1
    line.xValueAxis.labelTextFormat = lambda x: fechas[int(x)].strftime('%H:%M') if 0 <= int(x) < len(fechas) else ''
    line.xValueAxis.labels.angle = 0
    line.xValueAxis.labels.dy = -15
    line.xValueAxis.labels.dx = -15

    line.yValueAxis = YValueAxis()
    line.yValueAxis.valueMin = min(valores) - 1
    line.yValueAxis.valueMax = max(valores) + 1
    line.yValueAxis.labelTextFormat = '%2.2f'

    drawing.add(line)

    # Crear estilos
    styles = getSampleStyleSheet()
    header = Paragraph("Reporte de Lecturas", styles['Title'])
    description = Paragraph("Este es un reporte generado automáticamente que contiene las lecturas de los sensores.", styles['BodyText'])
    footer = Paragraph("Generado por IoT SENA", styles['Normal'])

    elements = [header, Spacer(1, 12), description, Spacer(1, 12), drawing, Spacer(1, 12), table, Spacer(1, 12), footer]
    doc.build(elements)

    buffer.seek(0)
    response.write(buffer.read())
    buffer.close()

    return response

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save
                login(request, user)
                return redirect('perfil')
            except:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": 'el usuario ya existe'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            "error": 'Las contraseñas no coinciden'
        })

def signout(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    clientes = Cliente.objects.filter(user=request.user)
    granjas = Granja.objects.all().prefetch_related('instalaciones__sensores').filter(cliente__user=request.user)
    instalacion = Instalacion.objects.filter(granja__cliente__user=request.user)
    return render(request, 'Dashboard.html',{
        'clientes': clientes,
        'granjas' : granjas,
        'instalaciones': instalacion
    })

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                "error": 'Username o password is incorrect'
            })
        else:
            login(request, user)
            return redirect('Dashboard')

@login_required
def cliente(request):
    clientes = Cliente.objects.filter(user=request.user)
    if clientes:
        return redirect('Dashboard')
    else:        
        return render(request, 'complete_perfil.html', {
            'form': ClienteForm
        })

@login_required
def complete_perfil(request):
    try:
        form = ClienteForm(request.POST)
        new_cliente = form.save(commit=False)
        new_cliente.user = request.user
        new_cliente.save()
        return redirect('perfil')
    except ValueError:
        return render(request,'complete_perfil.html',{
            'form' : ClienteForm,
            'error' : 'Ingrese datos correctos'
        })

@login_required
def sensor_detail(request, sensor_id):
    if request.method == 'GET':
        clientes = Cliente.objects.filter(user=request.user)
        lecturas = Lectura.objects.filter(sensor=sensor_id).order_by('hora')
        horas = [lectura.hora.strftime('%H:%M:%S') for lectura in lecturas]
        valores = [float(lectura.valor) for lectura in lecturas]
        granjas = Granja.objects.all().prefetch_related('instalaciones__sensores').filter(cliente__user=request.user)

        context = {
            'clientes': clientes,
            'granjas': granjas,
            'horas': horas,
            'valores': valores,
            'lecturas': lecturas,
            'sensor': Sensor.objects.get(pk=sensor_id)
        }        
        return render(request, 'sensor_detail.html', context)
@login_required
def get_lecturas(request,sensor_id):
    if request.method == 'GET':
        lecturas = Lectura.objects.filter(sensor=sensor_id).values('valor','hora')
        lista_lecturas = list(lecturas)    
        return JsonResponse({'lecturas': lista_lecturas})

@login_required
def granja_create(request):
    
    if request.method == 'GET':
        return render(request, 'granga_create.html',{
            'form' : GranjaForm
        })
    else:
        try:
            form = GranjaForm(request.POST)
            new_granja = form.save(commit=False)
            new_granja.cliente = Cliente.objects.get(user=request.user)
            new_granja.save()
            messages.success(request, '¡Granja Registrada!')
            return redirect('granjas')
        except ValueError:
            return render(request, 'granja_create.html',{
                'error': 'ingrese datos validos'
            })

@login_required   
def instalacion_create(request):
    cliente = Cliente.objects.get(user=request.user)
    if request.method == 'POST':
        try:
            form = InstalacionForm(request.POST, cliente=cliente)
            if form.is_valid():
                form.save()
                messages.success(request,'¡instalacion Registrada!')
                return redirect('granjas')  # Redirige a una vista de lista de instalaciones o donde quieras  
        except ValueError:
            return redirect('instalacion_create')
    else:
        form = InstalacionForm(cliente=cliente)
    
    return render(request, 'instalacion_create.html', {
        'form': form})
@login_required
def sensor_create(request):
    cliente = Cliente.objects.get(user=request.user)
    if request.method == 'POST':
        form = SensorForm(request.POST, cliente=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Sensor creado!')
            return redirect('granjas')
    else:
        form = SensorForm(cliente=cliente)
    return render(request, 'sensor_create.html', {'form': form})

@login_required
def sensor_update(request, sensor_id):
    if request.method == 'GET':
        sensor = get_object_or_404(Sensor, pk=sensor_id, instalacion__granja__cliente__user = request.user)
        form = SensorForm(instance=sensor)
        return render(request, 'sensor_update.html',{
            'sensor': sensor,
            'form' : form
        })
    else:
        try:
            sensor = get_object_or_404(Sensor, pk=sensor_id, instalacion__granja__cliente__user=request.user)
            form = SensorForm(request.POST, instance=sensor)
            form.save()
            messages.success(request, 'Sensor actualizado')
            return redirect('granjas')
        except ValueError:
            return render(request, 'sensor_update.html',{
                'instalacion': sensor,
                'form': form,
                'error':"Error al actualizar"
            })

@login_required        
def sensor_delete(request, sensor_id):
    sensor = get_object_or_404(Sensor, pk=sensor_id, instalacion__granja__cliente__user=request.user)
    if request.method == 'POST':
        sensor.delete()
        messages.success(request, 'sensor Eliminado!')
        return redirect('granjas')
@login_required
def granjas(request):
    granjas = Granja.objects.filter(cliente = Cliente.objects.get(user=request.user))
    return render(request, 'granjas.html',{
        'granjas':granjas
    })

@login_required
def instalaciones(request, granja_id):
    insta_list = Instalacion.objects.filter(granja=granja_id)
    granja = Granja.objects.get(pk=granja_id)
    return render(request, 'instalaciones.html',{
        'instalaciones': insta_list,
        'nombre_granja': granja.nombre
    })

@login_required
def instalacion_detail(request, instalacion_id):
    if request.method == 'GET':
        instalacion = get_object_or_404(Instalacion, pk=instalacion_id, granja__cliente__user = request.user)
        form = InstalacionForm(instance=instalacion)
        return render(request, 'instalacion_detail.html',{
            'instalacion': instalacion,
            'form' : form
        })
    else:
        try:
            instalacion = get_object_or_404(Instalacion, pk=instalacion_id, granja__cliente__user=request.user)
            form = InstalacionForm(request.POST, instance=instalacion)
            form.save()
            messages.success(request, 'Instalacion modificada')
            return redirect('granjas')
        except ValueError:
            return render(request, 'instalacion_detail.html',{
                'instalacion': instalacion,
                'form': form,
                'error':"Error al actualizar"
            })

@login_required        
def instalacion_delete(request, instalacion_id):
    instalacion = get_object_or_404(Instalacion, pk=instalacion_id, granja__cliente__user=request.user)
    if request.method == 'POST':
        instalacion.delete()
        messages.success(request, 'Instalacion Eliminada!')
        return redirect('granjas')

@login_required
def sensores(request, instalacion_id):
    sensor_list = Sensor.objects.filter(instalacion=instalacion_id)
    instalacion = Instalacion.objects.get(pk=instalacion_id)
    return render(request, 'sensores.html',{
        'sensores': sensor_list,
        'nombre_instalacion': instalacion.referencia
    })

@login_required
def granja_detail(request, granja_id):
    if request.method == 'GET':
        granja = get_object_or_404(Granja, pk=granja_id, cliente__user = request.user)
        form = GranjaForm(instance=granja)
        return render(request, 'granja_detail.html',{
            'granja': granja,
            'form' : form
        })
    else:
        try:
            granja = get_object_or_404(Granja, pk=granja_id, granja__cliente__user=request.user)
            form = GranjaForm(request.POST, instance=granja)
            form.save()
            messages.success(request, 'Granja modificada')
            return redirect('granjas')
        except ValueError:
            return render(request, 'granja_detail.html',{
                'granja': granja,
                'form': form,
                'error':"Error al actualizar"
            })

@login_required
def granja_delete(request, granja_id):
    granja = get_object_or_404(Granja, pk=granja_id, cliente__user=request.user)
    if request.method == 'POST':
        granja.delete()
        messages.success(request, 'Granja Eliminada!')
        return redirect('granjas')
