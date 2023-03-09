from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import ProceduresListView, update_sucursal_cameras_status, update_lost, update_one_lost
procedures_patterns = ([
    path('procedures/', login_required(ProceduresListView.as_view()), name='procedures'),
    path("camera_status/",update_sucursal_cameras_status,name="update_sucursal_cameras_status"),
    path("camera_video_lost/",update_lost,name="update_lost"),
    path("camera_update_one_lost/",update_one_lost,name="update_one_lost"),


], 'procedures')


