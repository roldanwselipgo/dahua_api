# Create your tasks here

from celery import shared_task
import time
from core.dahuaClasses.dahua_class import Dahua
from core.db import BDBDatabase
from core.dahuaClasses.dahua_config import Config as Conf

if 0:
    bd = BDBDatabase()

@shared_task(name="GetMediaEncode", time_limit=4)
def GetMediaEncode(host, port, user, password):
    dvr = Dahua(host, port, user, password)
    #video_encode_settings = dvr.GetMediaEncode() 
    config = Conf({},{},dvr)
    #---------- Obtener Configuracion de video -------------
    result =  config.GetMediaEncodeConfig(0,0)
    return result

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