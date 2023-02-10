from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import DeviceListView,DeviceDetailView,DeviceCreateView, DefaultConfigTemplateView, DeviceUpdateView, DeviceDeleteView, update_one
device_patterns = ([
    path('devices/', login_required(DeviceListView.as_view()), name='devices'),
    path('device/<int:pk>', login_required(DeviceDetailView.as_view()), name='device'),
    path('devices/create/', login_required(DeviceCreateView.as_view()), name='create'),
    path('device/update/<int:pk>', login_required(DeviceUpdateView.as_view()), name='update'),
    path('device/delete/<int:pk>', login_required(DeviceDeleteView.as_view()), name='delete'),
    path('device/videoEncode/update-one', update_one, name='update-one'),
    path('device/videoEncode/device=<int:device>', login_required(DefaultConfigTemplateView.as_view()), name='video-encode'),
], 'device')