"""prueba_elipgo URL Configuration

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
from django.urls import path, include
from django.contrib.auth import urls
from core.urls import core_patterns
#from monitor.urls import camera_patterns
from sitios.urls import sitio_patterns
from comparator.urls import comparator_patterns
from device.urls import device_patterns
from logs.urls import logs_patterns
from procedures.urls import procedures_patterns
from sucursales.urls import sucursal_patterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include(urls)),
    path('', include(core_patterns)),
#    path('', include(camera_patterns)),
    path('', include(sitio_patterns)),
    path('', include(comparator_patterns)),
    path('', include(device_patterns)),
    path('', include(logs_patterns)),
    path('', include(procedures_patterns)),
    path('', include(sucursal_patterns)),
    
]



