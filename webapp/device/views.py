from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse

from datetime import datetime
import os
import shutil
from .models import Device, DefaultConfig
from .forms import DeviceForm, DefaultConfigForm
import requests,json
from requests.auth import HTTPDigestAuth

from core.dahuaClasses.dahua_config import Config as Conf
from core.dahuaClasses.dahua_class import Dahua


from core.db import BDBDatabase
# Create your views here.

class DeviceDetailView(DetailView):
    """ Vista encargada de detallar el dispositivo seleccionado """
    model = Device
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #---------- Conexion a device -------------
        host = self.object.ip
        #port = 8011
        port = self.object.puerto
        user = self.object.usuario
        password = self.object.password
        dvr = Dahua(host, port, user, password) 
        general = dvr.GetGeneralConfig()
        device_type = dvr.GetDeviceType()
        device_type = device_type['type']  if 'type' in device_type else ""
        hardware_version = dvr.GetHardwareVersion()
        hardware_version = hardware_version['version']  if 'version' in hardware_version else ""
        serial_number = dvr.GetSerialNumber()
        serial_number = serial_number['sn']  if 'sn' in serial_number else ""
        current_time = dvr.GetCurrentTime()
        

        locales = "device1.obtener_locales_config()"
        di = dvr.GetDeviceInfo() 
        video_encode_settings = dvr.GetMediaEncode() 
        snapshot = dvr.GetSnapshot() 
        print("snap", snapshot.raw)
        print("gral", general)
        if snapshot.status_code == 200:
            #print(video_encode_settings, type(video_encode_settings))
            with open("device/static/device/snapshot.jpg", 'wb') as f:
                snapshot.raw.decode_content = True
                shutil.copyfileobj(snapshot.raw, f) 
        context['general']=general
        context['current_time']=current_time
        context['locales']=locales
        context['device_type']=device_type
        context['serial_number']=serial_number
        context['hardware_version']=hardware_version
        context['video_encode_settings']=video_encode_settings
        return context


class DeviceListView(ListView):
    """ Vista encargada de listar los dispositivos registrados """
    model = Device
    def get_queryset(self):
        device=Device.objects.all()
        return device

class DeviceCreateView(CreateView):
    model = Device
    form_class = DeviceForm
    success_url = reverse_lazy('device:devices')

class DeviceUpdateView(UpdateView):
    model = Device
    form_class = DeviceForm
    template_name_suffix = '_update_form'
    def get_success_url(self):
        return reverse_lazy('device:update', args=[self.object.id]) + '?ok'

class DeviceDeleteView(DeleteView):
    model = Device
    success_url = reverse_lazy('device:devices')


def videoencodeform(request):
    videoencodeform_form = ConfigForm()
    return render(request, "device/videoencode_form.html", {"form":videoencodeform_form})

def update_one(request):
    print(f"update_one()")
    if request.method == "GET":
        print("Entamos a get")
        #form = ConfigForm(data=self.request.GET)
        channel = request.GET.get('channel','')
        key = request.GET.get('key','')
        val = request.GET.get('val','')
        stream = request.GET.get('stream','')
        device_id = request.GET.get('device_id','')
        if val and key and device_id:
            print("Data: ", channel, key, val)
            device=Device.objects.filter(id = device_id).first()
            print(device.ip)
            print(device.puerto)

            id = device.id
            host = device.ip
            port = device.puerto
            user = device.usuario
            password = device.password

            dvr = Dahua(host, port, user, password)
            if key == "Compression":
                values = val.split(" ")
                if len(values) == 2:
                    print("A punto de mandar Profiles: ", values)
                    dvr.SetOneMediaEncode(int(channel),0,"Compression",values[0],stream)
                    dvr.SetOneMediaEncode(int(channel),0,"Profile",values[1],stream)
                    return HttpResponse("Update one ", content_type='text/plain')
            dvr.SetOneMediaEncode(int(channel),0,key,val,stream)
    return HttpResponse("Update one ", content_type='text/plain')


class DefaultConfigTemplateView(TemplateView):
    template_name = "device/videoencode_detail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        device_id = None
        if "device" in self.request.path:
            path = self.request.path.split("=")
            device_id = path[1]
        device=Device.objects.filter(id = device_id).first()
        id = device.id
        host = device.ip
        port = device.puerto
        user = device.usuario
        password = device.password
        dvr = Dahua(host, port, user, password)

        default_media_config = {}
        default_general_config = {}
        #Media config
        default_config=DefaultConfig.objects.all().first()
        default_media_config["Compression"] = default_config.Compression
        default_media_config["resolution"] = default_config.resolution
        default_media_config["SmartCodec"] = "Off"
        default_media_config["FPS"] = default_config.FPS
        default_media_config["BitRateControl"] = default_config.BitRateControl
        default_media_config["Quality"] = default_config.Quality
        default_media_config["BitRate"] = default_config.BitRate
        default_media_config["VideoEnable"] = default_config.VideoEnable
        #General config
        default_general_config["Language"] = default_config.Language
        #Llenar form con valores por defecto
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
            "CurrentTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        form = DefaultConfigForm(default_data)

        #---------- Obtener Configuracion de video 
        config = Conf(default_media_config, default_general_config, dvr)
        channels = config.ChannelDetect()
        array_config = config.GetMediaEncodeConfigCapability()
        langauge = config.getLanguage()
        current_time = config.getCurrentTime()
        device_type = config.getDeviceType()
        print("Channels >> ", channels)                  
        print("Language >> ", langauge)                  
        print("CurTime >> ", current_time)                  
        print("Device Type >> ", device_type)    
        device_type_name = 'DVR' if 'DH-' in device_type else "Device" 
        storage_info = config.getHDDevInfo()

        #print("Array config: ", array_config)


        if self.request.method == "GET":
            if self.request.GET.get('snapshots',''):
                #GetSnapshot
                paths = []
                for channel in channels:
                    channel = channel + 1
                    snapshot = dvr.GetSnapshot(channel) 
                    if snapshot.status_code == 200:
                        print(f"device/static/device/snapshots/ch{channel}.jpg")
                        print(f"device/static/device/snapshots/ch{channel}.jpg")
                        print(f"device/static/device/snapshots/ch{channel}.jpg")
                        print(f"device/static/device/snapshots/ch{channel}.jpg")
                        with open(f"device/static/device/snapshots/ch{channel}.jpg", 'wb') as f:
                            snapshot.raw.decode_contesnt = True
                            shutil.copyfileobj(snapshot.raw, f)
                            path = f"ch{channel}"
                            paths.append(path)
                context['snapshots'] = paths
            if form.is_valid():
                if self.request.GET.get('checkbox-time',''):
                    print("Enviar hora actual")
                    config.setCurrentTime()
                else:
                    print("Enviar hora del formulario", self.request.GET.get('CurrentTime','') )
                    config.setCurrentTime(self.request.GET.get('CurrentTime',''))
                    print(self.request.GET.get('CurrentTime',''))
                #if self.request.GET.get('Language',''):
                config.default_general_config["Language"] = self.request.GET.get('Language','')
                config.setLanguage()

                #---------- Actualizar configuracion si llego la peticion-------------
                print("Comenzar actualizacion") 
                channels_count = len(channels)
                if channels_count: 
                    for channel in range(0,channels_count):
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
                            if self.request.GET.get('mainstream',''):
                                print("Se incluye mainstream")
                                config.setDefaultMediaEncode(channel,0, "MainFormat")
                            if self.request.GET.get('substream',''):
                                print("Se incluye substream")
                                config.setDefaultMediaEncode(channel,0, "ExtraFormat")
                            
                    #----------Volver a obtener Configuracion de video -------------
                    if self.request.GET.get('Compression',''):
                        #channels = config.ChannelCount()
                        array_config = config.GetMediaEncodeConfigCapability()
            else:
                print(form.is_valid())

        context['id']=id
        context['ip']=host
        context['device_type']=device_type
        context['device_type_name']=device_type_name
        context['language']=langauge
        context['current_time']=current_time
        context['storage_info']=storage_info
        context['channels']=channels
        context['channels_reverse']=channels[::-1]
        context['array_config']=array_config
        context['form']=form
        return context

