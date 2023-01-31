from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
import os
import shutil
from .models import Camera, Config
from .forms import CameraForm, ConfigForm
import requests,json
from requests.auth import HTTPDigestAuth

from monitor.Monitor.Interfaz import Interfaz
from monitor.Monitor.Comunicacion import Comunicacion
from monitor.Monitor.Variable import Variable
from monitor.Monitor.Camera import Camera as Cam

from monitor.dahuaClasses.dahua_config import Config as Conf
from monitor.dahuaClasses.dahua_class import Dahua

from monitor.db import BDBDatabase



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
        bd = BDBDatabase()
        vc = Config.objects.filter(id=1).first()

        """proyecto = 'MC'
        id_sitio = 675
        ip = f"mc{id_sitio}.c5cdmx.elipgodns.com:8011"
        status = 'ups'
        is_alive = None
        last_update = "2022-08-13 21:02:45"
        vc = Config.objects.filter(id=1).first()
        obj, created = Sitio.objects.update_or_create(
                sitio=id_sitio,proyecto=proyecto, ip=ip,
                status=status,is_alive=is_alive,last_update=last_update,
                videoencode_config_id=vc
            )
        print(obj,created)"""

        if bd:
            #print("Conection success mysql")
            sitios = bd.GetSitios()
            for sitio in sitios:
                if 0:
                #if len(sitio):
                    proyecto = sitio[0]
                    id_sitio = sitio[1]
                    ip = f"mc{id_sitio}.c5cdmx.elipgodns.com:8011"
                    status = sitio[3]
                    is_alive = sitio[4]
                    last_update = sitio[5]
                    data = {
                        'sitio':id_sitio,
                        'proyecto':proyecto,
                        'ip':ip,
                        'status':status,
                        'is_alive':is_alive,
                        'last_update':last_update,
                        'videoencode_config_id':vc,
                    }
                    print(sitio,len(sitio))
                    print(id_sitio,proyecto,ip,status,is_alive,last_update,vc)
                    #obj, created = Sitio.objects.update_or_create(data)
                    try:
                        obj, created = Sitio.objects.update_or_create(
                            sitio=id_sitio,proyecto=proyecto, ip=ip,
                            status=status,is_alive=is_alive,last_update=last_update,
                            videoencode_config_id=vc
                        )
                        print(obj,created)
                    except:
                        print("Failed Unique constraint >> ", sitio)
            #context['sitios'] = Sitio.objects.all()
            context['sitios'] = ""
        return context

class CameraCreateView(CreateView):
    model = Camera
    form_class = CameraForm
    success_url = reverse_lazy('camera:cameras')

def videoencodeform(request):
    videoencodeform_form = ConfigForm()
    return render(request, "monitor/videoencode_form.html", {"form":videoencodeform_form})

class ConfigDetailView(DetailView):
    """ Vista encargada de mostrar la configuracion de video """
    model = Config
    #form_class = ConfigForm
    #success_url = reverse_lazy('camera:video-encode')
    #fields = ['Compression']
    #get_success_url = reverse_lazy('camera:video-encode')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cameras = []
        import time
        time.sleep(5)
        #Conexion
        #print("path:",self.request.path)

        #Obtener camara
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
        default_media_config["resolution"] = "720P"
        default_media_config["SmartCodec"] = "Off"
        default_media_config["FPS"] = 5
        default_media_config["BitRateControl"] = "VBR"
        default_media_config["Quality"] = 4
        default_media_config["BitRate"] = 512"""

        default_media_config["Compression"] = self.object.Compression
        default_media_config["resolution"] = self.object.CustomResolutionName
        default_media_config["SmartCodec"] = "Off"
        default_media_config["FPS"] = self.object.FPS
        default_media_config["BitRateControl"] = self.object.BitRateControl
        default_media_config["Quality"] = self.object.Quality
        default_media_config["BitRate"] = self.object.BitRate
        default_media_config["VideoEnable"] = self.object.VideoEnable
        
        #General config
        default_general_config["Language"] = "English"

        config = Conf(default_media_config, default_general_config, dvr)
        
       
        #---------- Obtener Configuracion de video -------------
        channels = config.ChannelCount()
        array_config = []
        if channels:
            for channel in range(0,channels):
                print("chian",channel)
                array_config.append(config.GetMediaEncodeConfig(channel,0))
        
        langauge = config.getLanguage()
        current_time = config.getCurrentTime()
        device_type = config.getDeviceType()
        print("Language >> ", langauge)                  
        print("CurTime >> ", current_time)                  
        print("Device Type >> ", device_type)    
        device_type_name = 'DVR' if 'DH-' in device_type else "Camera" 

        print("ARRAY CONFIG >>", array_config)

        #Validacion form
        default_data = {
            "Compression": default_media_config["Compression"],
            "resolution": default_media_config["resolution"],
            "SmartCodec": default_media_config["SmartCodec"],
            "FPS": default_media_config["FPS"],
            "BitRateControl": default_media_config["BitRateControl"],
            "Quality": default_media_config["Quality"],
            "BitRate": default_media_config["BitRate"],
            "VideoEnable": default_media_config["VideoEnable"],
            "Language": default_general_config["Language"],
            "VideoEnable": "true",
            "CurrentTime": current_time,
        }
        form = ConfigForm(default_data)
        if self.request.method == "GET":
            #form = ConfigForm(data=self.request.GET)
            if form.is_valid():
                print(">>>>Entrando a post:")
                compresion = self.request.GET.get('Compression','')
                checkbox = self.request.GET.get('0','')
                print("Values prob....",compresion,checkbox)

                #---------- Actualizar configuracion si llego la peticion-------------
                #tipo = self.request.GET.get('type')
                #ch = self.request.GET.get('channel')
                #if tipo and ch:
                print("Comenzar actualizacion") 
                channels = config.ChannelCount()
                if channels:
                    for channel in range(0,channels):
                        if self.request.GET.get(str(channel),''):
                            print("Configurando canal: ",channel)
                            config.default_media_config["Compression"] = self.request.GET.get('Compression','')
                            config.default_media_config["resolution"] = self.request.GET.get('resolution','')
                            config.default_media_config["FPS"] = self.request.GET.get('FPS','')
                            config.default_media_config["Quality"] = self.request.GET.get('Quality','')
                            config.default_media_config["BitRateControl"] = self.request.GET.get('BitRateControl','')
                            config.default_media_config["BitRate"] = self.request.GET.get('BitRate','')
                            config.default_media_config["VideoEnable"] = self.request.GET.get('VideoEnable','')
                            print(self.request.GET.get('VideoEnable',''), ">>>>>VideoEnable") 
                            print(self.request.GET.get('BitRate',''), ">>>>>BITR") 
                            config.default_general_config["Language"] = self.request.GET.get('Language','')
                            config.setDefaultMediaEncode(channel,0, "MainFormat")
                            config.setDefaultMediaEncode(channel,0, "ExtraFormat")
                            if self.request.GET.get('checkbox-time',''):
                                print("Enviar hora actual")
                                config.setCurrentTime()
                            else:
                                print("Enviar hora del formulario", self.request.GET.get('CurrentTime','') )
                                config.setCurrentTime(self.request.GET.get('CurrentTime',''))
                                print(self.request.GET.get('CurrentTime',''))
                            #config.setCurrentTime()
                            config.setLanguage()
                            
                    #----------Volver a obtener Configuracion de video -------------
                    if self.request.GET.get('Compression',''):
                        channels = config.ChannelCount()
                        array_config = []
                        if channels:
                            for channel in range(0,channels):
                                print("chian",channel)
                                array_config.append(config.GetMediaEncodeConfig(channel,0))

                            

            else:
                print(form.is_valid())


        configs_mainstream = []
        configs_substream = []

        context['device_type']=device_type
        context['device_type_name']=device_type_name
        context['language']=langauge
        context['current_time']=current_time
        context['channel_count']=len(array_config)
        context['array_config']=array_config
        context['form']=form
        return context

