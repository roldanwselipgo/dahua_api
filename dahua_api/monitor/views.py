from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
import os
import shutil
from .models import Camera
from .models import VideoEncode
from .forms import CameraForm, VideoEncodeForm
import requests,json
from requests.auth import HTTPDigestAuth

from monitor.Monitor.Interfaz import Interfaz
from monitor.Monitor.Comunicacion import Comunicacion
from monitor.Monitor.Variable import Variable
from monitor.Monitor.Camera import Camera as Cam

from monitor.DahuaClasses.dahua_config import Config
from monitor.DahuaClasses.dahua_class import Dahua



# Create your views here.
class StaffRequiredMixin(object):
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)
    

    
class CameraDetailView(DetailView):
    """ Vista encargada de detallar el dispositivo seleccionado """
    model = Camera
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ###-----Nueva estructura
        puerto = Interfaz("api")
        puerto.modificarConfiguracion(
                                    dispositivo = Interfaz.CAMARA_DAHUA, 
                                    protocolo = 'http', 
                                    servidor = 'elipgomexico.ddns.net', 
                                    puerto = '1938', 
                                    usuario = 'test', 
                                    password = 'test$2022'
                                    )
        comunicacion = Comunicacion ()
        puerto.inicializar()
        
        # Se crea y se configura el dispositivo
        camera1 = Cam("Camera 1", "CAM-001", "En camara")
        camera1.establecerPuerto(puerto)
        camera1.establecerComunicacion (comunicacion)
        
        general = camera1.obtener_datos_generales()
        current_time = camera1.obtener_current_time()
        locales = camera1.obtener_locales_config()
        device_type = camera1.obtener_device_type()
        machine_name = camera1.obtener_machine_name()
        
        camera1.actualizar_motion_settings(estado="true")
        motion_settings = camera1.obtener_motion_settings()

        snapshot = camera1.obtener_snapshot()
        with open("monitor/static/monitor/snapshot.jpg", 'wb') as f:
            snapshot.raw.decode_content = True
            shutil.copyfileobj(snapshot.raw, f)  


        context['general']=general
        context['current_time']=current_time
        context['locales']=locales
        context['device_type']=device_type
        context['machine_name']=machine_name.text
        context['motion_settings']=motion_settings
        return context


class CameraListView(ListView):
    """ Vista encargada de listar los dispositivos registrados """
    model = Camera
    def get_queryset(self):
        camera=Camera.objects.all()
        return camera

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cameras = []
        for camera in self.object_list:
            
            puerto = Interfaz("api {}".format(camera.usuario))
            puerto.modificarConfiguracion(
                                    dispositivo = Interfaz.CAMARA_DAHUA, 
                                    protocolo = 'http', 
                                    servidor = camera.ip, 
                                    puerto = camera.puerto, 
                                    usuario = camera.usuario, 
                                    password = camera.password,
                                    )
            comunicacion = Comunicacion ()
            puerto.inicializar()
            cam = Cam("Camera 1", "CAM-{}".format(camera.id), "En camara")
            cam.establecerPuerto(puerto)
            cam.establecerComunicacion (comunicacion)
            if cam.obtener_serial_no():
                #print("sn",cam.obtener_serial_no())
                serial_no = cam.variables[2].obtenerDescripcion()
                cameras.append(serial_no)
                camera.serial_no = serial_no
                camera.save()
            else:
                camera.serial_no = '0'
                camera.save()

        context['cameras_serial_no']=cameras
        return context

class CameraCreateView(CreateView):
    model = Camera
    form_class = CameraForm
    success_url = reverse_lazy('camera:cameras')

def videoencodeform(request):
    videoencodeform_form = VideoEncodeForm()
    return render(request, "monitor/videoencode_form.html", {"form":videoencodeform_form})

class VideoEncodeDetailView(DetailView):
    """ Vista encargada de mostrar la configuracion de video """
    model = VideoEncode
    form_class = VideoEncodeForm


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cameras = []
        #context['callback_form'] = CallBackForm(initial={'HouseId': self.object.id})

        #Conexion
        print("ol",self.request)
        print("ol",self.request.GET)
        print("ol",self.request.GET.get('typesss') )
        print("ol",self.request.path)


        camara_id = None
        if "camera" in self.request.path:
            path = self.request.path.split("=")
            camara_id = path[1]

        print("camara_id",camara_id)


        camera=Camera.objects.filter(id = camara_id).first()
        print(camera.ip)
        print(camera.puerto)

        host = camera.ip
        port = camera.puerto
        user = camera.usuario
        password = camera.password

        #host = "10.200.3.20"
        #port = 1938
        #user = "admin"
        #password = "Elipgo$123

        #---------- Conexion a camara -------------
        dvr = Dahua(host, port, user, password)

        #Media config
        default_media_config = {}
        default_general_config = {}
        
        print("compression: ",self.object.Compression)

        """default_media_config["Compression"] = "H.264"
        default_media_config["CustomResolutionName"] = "720P"
        default_media_config["SmartCodec"] = "Off"
        default_media_config["FPS"] = 5
        default_media_config["BitRateControl"] = "VBR"
        default_media_config["Quality"] = 4
        default_media_config["BitRate"] = 512"""

        default_media_config["Compression"] = self.object.Compression
        default_media_config["CustomResolutionName"] = self.object.CustomResolutionName
        default_media_config["SmartCodec"] = "Off"
        default_media_config["FPS"] = self.object.FPS
        default_media_config["BitRateControl"] = self.object.BitRateControl
        default_media_config["Quality"] = self.object.Quality
        default_media_config["BitRate"] = self.object.BitRate
        

        #General config
        default_general_config["Language"] = "English"

        config = Config(default_media_config, default_general_config, dvr)
        
        


        #---------- Actualizar configuracion si llego la peticion-------------
        tipo = self.request.GET.get('type')
        channel = self.request.GET.get('channel')
        if tipo and channel:
            print("Comenzar actualizacion") 
            #config.set_default_config()
            config.set_default_config_all_channels_all_streams()

        
        #---------- Obtener Configuracion de video -------------
        current_config_mainstream, current_config_substream = config.GetMediaEncodeAutoConfig(0,0)
        print("CCF",current_config_mainstream, ":" ,current_config_substream)


        
        
        context['current_config_mainstream']=current_config_mainstream
        context['current_config_substream']=current_config_substream
        return context
