from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import ProceduresListView, update_sucursal_cameras_status, update_lost, update_one_lost, summary, update_sucursales_status, update_lost_dahua, update_noip_status, DescargarArchivoView
procedures_patterns = ([
    #path('procedures/', login_required(ProceduresListView.as_view()), name='procedures'),
    path('procedures/', ProceduresListView.as_view(), name='procedures'),
    path("camera_status/",update_sucursal_cameras_status,name="update_sucursal_cameras_status"),
    path("camera_video_lost/",update_lost,name="update_lost"),
    path("camera_video_lost_dahua/",update_lost_dahua,name="update_lost_dahua"),
    path("camera_update_one_lost/",update_one_lost,name="update_one_lost"),
    path("summary/",summary,name="summary"),
    path("update_sucursales_status/",update_sucursales_status,name="update_sucursales_status"),
    path("update_noip_status/",update_noip_status,name="update_noip_status"),
    path('descargar-archivo/', DescargarArchivoView.as_view(), name='descargar_archivo'),

], 'procedures')


