"""IoT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from sensores import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.signout, name='logout'),
    path('Dashboard/', views.dashboard, name='Dashboard'),
    path('sensor/<int:sensor_id>', views.sensor_detail, name='sensor_detail'),
    path('granja/create', views.granja_create, name='granja_create'),
    path('instalacion/create', views.instalacion_create, name='instalacion_create'),
    path('instalacion/<int:instalacion_id>/', views.instalacion_detail, name='instalacion_detail'),
    path('instalacion/<int:instalacion_id>/delete', views.instalacion_delete, name='instalacion_delete'),
    path('sensor/create', views.sensor_create, name='sensor_create'),
    path('sensor/<int:sensor_id>/update', views.sensor_update, name='sensor_update'),
    path('sensor/<int:sensor_id>/delete', views.sensor_delete, name='sensor_delete'),
    path('get_lecturas/<int:sensor_id>/', views.get_lecturas, name='get_lecturas'),
    path('granjas/', views.granjas, name='granjas'),
    path('granja/<int:granja_id>/', views.granja_detail, name='granja_detail'),
    path('granja/<int:granja_id>/delete', views.granja_delete, name='granja_delete'),
    path('instalaciones/<int:granja_id>', views.instalaciones, name='instalaciones'),
    path('sensores/<int:instalacion_id>', views.sensores, name='sensores'),
    path('signin/', views.signin, name='signin'),
    path('perfil/', views.cliente, name='perfil'),
    path('cliente_create', views.complete_perfil, name='cliente_create'),
    path('generate_pdf/<int:sensor_id>/', views.generate_pdf, name='generate_pdf')
]
