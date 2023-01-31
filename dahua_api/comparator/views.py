from django.shortcuts import render
from sitios.models import Sitio, Config, Stream, Channel
from .models import SitioB, ConfigB, StreamB, ChannelB
from django.views.generic.list import ListView
from django.urls import reverse, reverse_lazy
from core.dahuaClasses.dahua_class import Dahua
from core.db import BDBDatabase
from core.dahuaClasses.dahua_config import Config as Conf
from sitios import tasks
import time
from django.http import HttpResponse
# Create your views here.


class SitioBListView(ListView):
    """ Vista encargada de listar los dispositivos registrados """
    model = Sitio
    def get_queryset(self):
        sitios=SitioB.objects.all()
        #for sitio in sitios:
        #    print(">", sitio)
        return sitios


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = []
        conf = ""
        #Obtener configuraciones del sitio

        if 1:
            #for i in range
            sitios=SitioB.objects.all().order_by('sitio')[:1000]
            for sitio in sitios:
                configs = {}
                conf = "<br>"
                #print(sitio.ip, sitio.status)
                channels=ChannelB.objects.filter(sitio=sitio)
                #print(channels)
                for channel in channels:
                    #print(channel, channel.number)
                    conf = conf + f"<h5>Channel {channel.number}: <h5>"
                    #print (channel.streams[0], type(channel.streams))
                    #stream = StreamB.objects.filter(channel.streams)
                    streams = channel.streams.all().order_by('name')
                    
                    for stream in streams:
                        st=StreamB.objects.filter(id=stream.id).first()
                        cf=ConfigB.objects.filter(id=st.id_config.id).first()
                        #print("stream>",st,cf.Compression)
                        conf = conf + f"<h6>{st.name}:</h6> "
                        conf = conf + f"Compression: {cf.Compression} <br>"
                        conf = conf + f"Resolution: {cf.resolution} <br>"
                        conf = conf + f"SmartCodec: {cf.SmartCodec} <br>"
                        conf = conf + f"FPS: {cf.FPS} <br>"
                        conf = conf + f"BitRateControl: {cf.BitRateControl} <br>"
                        conf = conf + f"Quality: {cf.Quality} <br>"
                        conf = conf + f"BitRate: {cf.BitRate} <br>"
                        conf = conf + f"VideoEnable: {cf.VideoEnable} <br>"
                        conf = conf + f"Language: {cf.Language} <br>"
                        conf = conf + f"CurrentTime: {cf.CurrentTime} <br>"
            #print(conf)
                configs["ip"] = sitio.ip
                configs["status"] = sitio.status
                configs["last_update"] = sitio.last_update
                #print(conf)
                configs["conf"] = conf
                data.append(configs)
        context["configs"] = data
        print("Finished")
        return context

                    
        sitios=SitioB.objects.all()

        
        return context
        
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

        """
        
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
        """

