from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import ServicioListView,ServicioDetailView
servicio_patterns = ([
    path('servicios/', login_required(ServicioListView.as_view()), name='servicios'),
    path('servicio/<int:pk>', login_required(ServicioDetailView.as_view()), name='servicio'),

], 'servicio')