from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import DeviceListView,DeviceDetailView,DeviceCreateView, DefaultConfigTemplateView
device_patterns = ([
    path('devices/', login_required(DeviceListView.as_view()), name='devices'),
    path('device/<int:pk>', login_required(DeviceDetailView.as_view()), name='device'),
    path('devices/create/', login_required(DeviceCreateView.as_view()), name='create'),
    path('videoEncode/device=<int:device>', login_required(DefaultConfigTemplateView.as_view()), name='video-encode'),
], 'device')