from django.shortcuts import render
from .models import Sitio
from .models import Config, Stream, Channel
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse, reverse_lazy
from core.dahuaClasses.dahua_class import Dahua
from core.db import BDBDatabase
from core.dahuaClasses.dahua_config import Config as Conf
from sitios import tasks
import time
from django.http import HttpResponse
import logging
import shutil
# Create your views here.


class SitioListView(ListView):
    """ Vista encargada de listar los dispositivos registrados """
    model = Sitio
    def get_queryset(self):
        sitios=Sitio.objects.all()
        return sitios


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sitios = []
        
        """
        proyecto = 'MF'
        id_sitio = 1
        ip = f"mc{id_sitio}.c5cdmx.elipgodns.com"
        status = 'ups'
        is_alive = None
        last_update = "2022-08-13 21:02:45"
        vc = Config.objects.filter(id=1).first()
        obj, created = Sitio.objects.update_or_create(
                sitio=id_sitio,proyecto=proyecto, ip=ip,
                status=status,is_alive=is_alive,last_update=last_update,
                videoencode_config_id=vc
            )"""

        
        if 0:
            #print("Conection success mysql")
            bd = BDBDatabase()
            vc = Config.objects.filter(id=1).first()
            sitios = bd.GetSitios()
            for sitio in sitios:
                if 0:
                #if len(sitio):
                    proyecto = sitio[0]
                    id_sitio = sitio[1]
                    ip = f"mc{id_sitio}.c5cdmx.elipgodns.com"
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
                    #Update_or_create
                    try:
                        item = Sitio.objects.get(sitio=id_sitio)
                    except Sitio.DoesNotExist:
                        Sitio.objects.create(sitio=id_sitio,proyecto=proyecto, ip=ip,
                            status=status,is_alive=is_alive,last_update=last_update,
                            videoencode_config_id=vc)
                    else:
                        item = Sitio.objects.filter(
                            sitio=id_sitio
                        ).update(
                            ip=ip, status=status, is_alive=is_alive,
                            last_update=last_update, videoencode_config_id=vc
                        )
                    print(item)
                    
            context['sitios'] = Sitio.objects.all()
        return context


class SitioDetail2View(DetailView):
    model = Sitio
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sitios = []
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
        dvr.GetMediaEncode() 



class SitioDetailView(DetailView):
    """ Vista encargada de detallar el dispositivo seleccionado """
    model = Sitio
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #---------- Conexion a device -------------
        host = self.object.ip
        port = 8011
        user = "admin"
        password = "Elipgo$123"
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

'''
class SitioDetailView(DetailView):
    """ Vista encargada de detallar el dispositivo seleccionado """
    model = Sitio
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        #---------- Conexion a camara -------------


        host = self.object.ip
        port = 8011
        user = "admin"
        password = "Elipgo$123"
        dvr = Dahua(host, port, user, password)
        

        
        general = "camera1.obtener_datos_generales()"
        current_time = "camera1.obtener_current_time()"
        locales = "camera1.obtener_locales_config()"
        device_type = "camera1.obtener_device_type()"
        machine_name = "camera1.obtener_machine_name()"
        
        #video_encode_settings = dvr.GetMediaEncode() 
        #print(video_encode_settings, type(video_encode_settings))
        print("QWESTAPASANDO")
        video_encode_settings = ""
        try: 
            result = tasks.GetAllMediaEncode.delay(host, port, user, password)
            video_encode_settings = result.get(timeout=5)
        #except TimeoutError as error:
        except:
            print("TimeoutError 5 secs")
        else:
            print("Result task Get all >>> ", video_encode_settings)

        """snapshot = camera1.obtener_snapshot()
        with open("monitor/static/monitor/snapshot.jpg", 'wb') as f:
            snapshot.raw.decode_content = True
            shutil.copyfileobj(snapshot.raw, f) """ 

        context['general']=general
        context['current_time']=current_time
        context['locales']=locales
        context['device_type']=device_type
        context['machine_name']="machine_name.text"
        context['video_encode_settings']=video_encode_settings
        return context
'''

def truncate_model(model):
    model.objects.all().delete()

def registrar_configuracion_sitio(configs, sitio):
    config_sitios = ""
    config_sitios = []
    id_sitio = sitio.sitio
    host = sitio.ip
    print(sitio.ip)
    if 1: 
        #result = tasks.GetMediaEncodeA.delay(host, port, user, password, id_sitio)
        #result = tasks.GetMediaEncodeA.delay(host, port, user, password, id_sitio)
        #configs = result.get(timeout=5)
        #configs = result.get()
        if configs:
            config_sitios.append(configs)
            for channels in configs:
                for stream in channels:
                    dict2 = {}
                    # Se pasa a entero ya que en ocasiones llega en float el valor de FPS
                    fps_stream=int(float(stream['FPS'])) if stream['FPS'] else None
                    quality_stream=int(float(stream['Quality'])) if stream['Quality'] else None
                    bitrate_stream=int(float(stream['BitRate'])) if stream['BitRate'] else None
                    dict2 = {
                    'Compression' : stream['Compression'],
                    'resolution' : stream['resolution'],
                    'FPS' : fps_stream,
                    'Quality' : quality_stream,
                    'BitRateControl' : stream['BitRateControl'],
                    'BitRate' : bitrate_stream
                    }
                    print("dict2>",dict2)
                    #print("stream>",stream)
                    if stream['Stream'] == "MainFormat":
                        config = None
                        # Buscamos si existe la configuracion, sino la creamos
                        try:
                            print("Antes de: ", dict2)
                            config = Config.objects.get(**dict2)
                            print("Se encontro Config>>>>")
                        except Config.DoesNotExist:
                            config = Config(**dict2)
                            print("Se crea nueva config", stream['Channel'], stream['Stream'], config )
                            config.save()
                        
                        # Buscamos si existe el stream, sino lo creamos
                        try:
                            streamsss = Stream.objects.filter(name="MainFormat", id_config=config)
                            print("Streamssss y cantidad y config", len(streamsss), streamsss, config)
                            stream_obj_main = Stream.objects.get(name="MainFormat", id_config=config)
                            print("Se encontro MainStream>>>>", stream_obj_main)
                        except Stream.DoesNotExist:
                            stream_obj_main = Stream(name="MainFormat", id_config=config)
                            print("Se crea nuevo Stream", stream['Channel'], stream['Stream'], stream_obj_main )
                            stream_obj_main.save()
                        
                        
                    elif stream['Stream'] == "ExtraFormat":
                        try:
                            config = Config.objects.get(**dict2)
                            print("Se encontro Config>>>>")
                        except Config.DoesNotExist:
                            config = Config(**dict2)
                            print("Se crea nueva config", stream['Channel'], stream['Stream'], config )
                            config.save()

                        
                        # Buscamos si existe el stream, sino lo creamos
                        try:
                            stream_obj_extra = Stream.objects.get(name="ExtraFormat", id_config=config)
                            print("Se encontro ExtraStream>>>>",stream_obj_extra)
                        except Stream.DoesNotExist:
                            stream_obj_extra = Stream(name="ExtraFormat", id_config=config)
                            print("Se crea nuevo Stream", stream['Channel'], stream['Stream'], stream_obj_extra )
                            stream_obj_extra.save()
                

                s = Sitio.objects.filter(sitio=id_sitio).first()
                print("Channel : > , id_sitio > , s > stream_obj >", channels[0]['Channel'], id_sitio, s, stream_obj_main, stream_obj_extra )

                #Buscamos si existe el canal, sino lo creamos 
                #try:
                #    s = Sitio.objects.filter(sitio=id_sitio).first()
                #    channel = Channel.objects.get(number=stream['Channel'], streams=stream_obj_main, sitio=s)
                #    print("Se encontro Channel>>>>")
                #except Channel.DoesNotExist:
                if 1:
                    channel = Channel(number=stream['Channel'], sitio = s)
                    channel.save()
                    #channel.sitios.add(s)
                    channel.streams.add(stream_obj_main,stream_obj_extra)
                    print("Se crea nuevo channel", stream['Channel'], channel )
                    #channel.save()
                    

    #except Exception as e:
        #logging.exception("La except es: ")
    #    print("Err: ", e, type(e))

def update_config_sites(request):
    #Borramos la configuracion existente
    Channel.objects.all().delete()
    Config.objects.all().delete()
    Stream.objects.all().delete()
    #return 0

    #sitios = Sitio.objects.filter(status="running").order_by('sitio')[:5]
    sitios = Sitio.objects.filter(status="running").order_by('sitio')
    print("len sitios: ",len(sitios)) 
    task_queue = []

    for sitio in sitios:
        print(sitio.ip)
        id_sitio = sitio.sitio
        host = sitio.ip
        port = 8011
        user = "admin"
        password = "Elipgo$123"
        #if 1:  
        task = tasks.GetMediaEncodeA.delay(host, port, user, password, id_sitio)
        task_queue.append((task,sitio))

    print("len task_queue:", len(task_queue))
    while len(task_queue):
        for i,task in enumerate(task_queue):
            #print("Scanning in: ", i)
            if task[0].ready():
                print(f"Tarea {task} terminada")
                try:
                    result = task[0].get()
                    #print("Resultado de tarea: ", result)
                    task_queue.remove(task)
                    print("\nlen task_queue:", len(task_queue))
                except Exception as e: 
                    print(f"Err en {task}: ", e)
                    task_queue.remove(task)
                    print("len task_queue:", len(task_queue))
                    break
                finally:
                    registrar_configuracion_sitio(result, task[1])
                    break

    return HttpResponse("Success "+str(len(sitios)), content_type='text/plain')
    

    for sitio in sitios:
        print(sitio.ip)
        id_sitio = sitio.sitio
        host = sitio.ip
        port = 8011
        user = "admin"
        password = "Elipgo$123"
        #if 1: 
        

            #print("Result task Get all >>> ", config_sitios)

    #for sitios in config_sitios:
    #    for channel in sitios:
            #print(channel)
    #        pass

    return HttpResponse(config_sitios, content_type='text/plain')
    #try: 
    #    result = tasks.GetAllMediaEncode.delay(host, port, user, password)
    #    video_encode_settings = result.get(timeout=5)
    ##except TimeoutError as error:
    #except:
    #    print("TimeoutError 5 secs")
    #else:
    #    print("Result task Get all >>> ", video_encode_settings)
    #return "<h1>Updating config sites...</h1>"