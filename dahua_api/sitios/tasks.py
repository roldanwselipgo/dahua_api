# Create your tasks here

from celery import shared_task
import time
from core.dahuaClasses.dahua_class import Dahua
from core.db import BDBDatabase
from core.dahuaClasses.dahua_config import Config as Conf
from .models import Config, Sitio, Channel, Stream


@shared_task(name="GetMediaEncodeA", time_limit=60)
def GetMediaEncodeA(host, port, user, password, id_sitio):
    try:
        dvr = Dahua(host, port, user, password)
        #video_encode_settings = dvr.GetMediaEncode() 
        config = Conf({},{},dvr)
        #---------- Obtener Configuracion de video -------------
        configs =  config.GetMediaEncodeConfig(0,0)
    except:
        return 0
    """if configs:
        #config_sitios.append(configs)
        for channels in configs:
            for stream in channels:
                dict2 = {}
                dict2 = {
                'Compression' : stream['Compression'],
                'resolution' : stream['resolution'],
                'FPS' : stream['FPS'],
                'Quality' : stream['Quality'],
                'BitRateControl' : stream['BitRateControl'],
                'BitRate' : stream['BitRate']
                }
                print("dict2>",dict2)
                print("stream>",stream)
                if stream['Stream'] == "MainFormat":
                    config = None
                    # Buscamos si existe la configuracion, sino la creamos
                    try:
                        config = Config.objects.get(**dict2)
                        print("Se encontro Config>>>>")
                    except Config.DoesNotExist:
                        config = Config(**dict2)
                        print("Se crea nueva config", stream['Channel'], stream['Stream'], config )
                        config.save()
                    
                    # Buscamos si existe el stream, sino lo creamos
                    try:
                        stream_obj_main = Stream.objects.get(name="MainFormat", id_config=config)
                        print("Se encontro Stream>>>>")
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
                        print("Se encontro Stream>>>>")
                    except Stream.DoesNotExist:
                        stream_obj_extra = Stream(name="ExtraFormat", id_config=config)
                        print("Se crea nuevo Stream", stream['Channel'], stream['Stream'], stream_obj_extra )
                        stream_obj_extra.save()
            

            s = Sitio.objects.filter(sitio=id_sitio).first()
            print("Channel : > , id_sitio > , s > stream_obj >", channels[0]['Channel'], id_sitio, s, stream_obj_main, stream_obj_extra )

            #Buscamos si existe el canal, sino lo creamos 
            try:
                s = Sitio.objects.filter(sitio=id_sitio).first()
                channel = Channel.objects.get(number=stream['Channel'], streams=stream_obj_main, sitio=s)
                print("Se encontro Channel>>>>")
            except Channel.DoesNotExist:
                channel = Channel(number=stream['Channel'], sitio = s)
                channel.save()
                #channel.sitios.add(s)
                channel.streams.add(stream_obj_main,stream_obj_extra)
                print("Se crea nuevo channel", stream['Channel'], channel )
                #channel.save()"""
    return configs

@shared_task(name="GetAllMediaEncode", time_limit=12)
def GetAllMediaEncode(host, port, user, password):
    dvr = Dahua(host, port, user, password)
    video_encode_settings = dvr.GetMediaEncode() 
    return video_encode_settings


@shared_task
def tsleep(t):
    time.sleep(t)
    return "tsleep 5 success"

@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


"""@shared_task
def count_widgets():
    return Widget.objects.count()


@shared_task
def rename_widget(widget_id, name):
    w = Widget.objects.get(id=widget_id)
    w.name = name
    w.save()"""