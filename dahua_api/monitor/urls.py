from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import CameraListView,CameraDetailView,CameraCreateView,VideoEncodeDetailView
camera_patterns = ([
    path('', CameraListView.as_view(), name='cameras'),
    path('camera/<int:pk>', CameraDetailView.as_view(), name='camera'),
    path('add-camera/', CameraCreateView.as_view(), name='add-camera'),
    path('videoEncode/<int:pk>/camera=<int:camera>', VideoEncodeDetailView.as_view(), name='video-encode'),

], 'camera')