from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import CameraListView,CameraDetailView,CameraCreateView,ConfigDetailView
camera_patterns = ([
    path('', login_required(CameraListView.as_view()), name='cameras'),
    path('camera/<int:pk>', login_required(CameraDetailView.as_view()), name='camera'),
    path('add-camera/', login_required(CameraCreateView.as_view()), name='add-camera'),
    path('videoEncode/<int:pk>/camera=<int:camera>', login_required(ConfigDetailView.as_view()), name='video-encode'),

], 'camera')