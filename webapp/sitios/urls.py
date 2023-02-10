from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import SitioListView,SitioDetailView, update_config_sites
sitio_patterns = ([
    path('sitios/', login_required(SitioListView.as_view()), name='sitios'),
    path('sitio/<int:pk>', login_required(SitioDetailView.as_view()), name='sitio'),
    path("update-config-sites",update_config_sites,name="update-config-sites",
),
    
], 'sitio')