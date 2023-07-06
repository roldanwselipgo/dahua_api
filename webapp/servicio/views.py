from .models import Servicio
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse, reverse_lazy
from core.dahuaClasses.dahua_class import Dahua
from core.dahuaClasses.dahua_config import Config as Conf
import time
from django.http import HttpResponse
import logging
import shutil
from core.database.db import DB
from datetime import datetime


class ServicioListView(ListView):
    """ Vista encargada de listar los dispositivos registrados """
    model = Servicio
    def get_queryset(self):
        servicios=Servicio.objects.all()
        return servicios


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        servicios=Servicio.objects.all()
        for servicio in servicios:
            print(servicio.servicio,"id")
            print(servicio.tabla,"tabla")
            print(servicio.columna,"columna")
            if 1:
                db = DB(host=f'{servicio.servidor}' , database=f'{servicio.bd}', user='elipgo', password='3l1pg0$123')
                db.open_connection()
                if db.connection.is_connected():
                    result = db.query_one(f"select {servicio.columna} from {servicio.bd}.{servicio.tabla} order by {servicio.columna} desc LIMIT 1;")
                    print("result",result)
                    if result:
                        print(result[0], type(result[0]))
                        now =  datetime.now()
                        resta = now - result[0]
                        tiempo_inactivo = resta.seconds-3600
                        print(now,result[0], resta.seconds, tiempo_inactivo)
                        print("comparacion de tolerancia: ",tiempo_inactivo, servicio.tiempo_de_toleracia)
                        if tiempo_inactivo > servicio.tiempo_de_toleracia:
                            print(f"Alerta servicio inactivo! : {servicio.nombre}, Ultima vez activo: {servicio.ultima_vez_activo}")
                            servicio.ultima_vez_activo = result[0]
                            servicio.status = "offline"
                            servicio.save()
                        else:
                            print(f" servicio activo! : {servicio.nombre}, Ultima vez activo: {servicio.ultima_vez_activo}")
                            servicio.status = "online"
                            servicio.ultima_vez_activo = result[0]
                            servicio.save()

                    else:
                        print("404 not found")

                    db.close_connection()
                else: 
                    print("No connection to DB")
                    return 0
            else:
                print("Sin conexion a DB")
            time.sleep(1)
        return context



class ServicioDetailView(DetailView):
    """ Vista encargada de detallar el dispositivo seleccionado """
    model = Servicio
    '''def get_context_data(self, **kwargs):
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
        return context'''

