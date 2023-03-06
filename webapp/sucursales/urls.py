from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import SucursalListView,SucursalDetailView
sucursal_patterns = ([
    path('sucursales/', login_required(SucursalListView.as_view()), name='sucursales'),
    path('sucursal/<int:pk>', login_required(SucursalDetailView.as_view()), name='sucursal'),
    #path("update-config-sites",update_config_sites,name="update-config-sites",
], 'sucursal')