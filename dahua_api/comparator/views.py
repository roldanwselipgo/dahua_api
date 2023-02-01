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


    def buscar_sitio_A(self):
        pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = []
        #dataA = []
        #conf = ""
        #Obtener configuraciones del sitio

        if 1:
            #for i in range
            sitiosB=SitioB.objects.all().order_by('sitio')[:1000]
            # sitiosA=Sitio.objects.all().order_by('sitio')[:1000]

            # #Pruebas de comparacion
            # #sitioPrueba=SitioB.objects.all().order_by('sitio')[:1000].first()
            # #print("SitioPrueba",sitioPrueba)
            # #sitioPruebaA=Sitio.objects.filter(sitio=sitioPrueba.sitio).first()
            # #print("Sitios Prueba", sitioPrueba, sitioPruebaA)
            # sitiosA = []
            # for sitioB in sitiosB:
            #     #sitioA=Sitio.objects.filter(sitio=sitioB.sitio).first()
            #     sitioA=Sitio.objects.filter(sitio=sitioB.sitio).first()
            #     sitiosA.append(sitioA) if sitioA else print("No haber sitio")
            
            # print("SitiosA: ",sitiosA)
            # print("Cantidad SitiosA: ",len(sitiosA))
                    

            # for (sitio,sitioA) in zip(sitiosB,sitiosA):
            #     #print(f"sitioB: {sitio} , sitioA:{sitioA}")
            #     pass

            for sitioB in sitiosB:
                sitioA=Sitio.objects.filter(sitio=sitioB.sitio).first()

                configs = {}
                confB = "<br>"
                confA = "<br>"
                #print(sitio.ip, sitio.status)
                channelsB=ChannelB.objects.filter(sitio=sitioB)
                channelsA=Channel.objects.filter(sitio=sitioA)
                #print(channels)
                for channelB in channelsB:
                    #print(channel, channel.number)
                    confB = confB + f"<h5>Channel {channelB.number}: <h5>"
                    #print (channel.streams[0], type(channel.streams))
                    #stream = StreamB.objects.filter(channel.streams)
                    streamsB = channelB.streams.all().order_by('name')
                    
                    for streamB in streamsB:
                        stb=StreamB.objects.filter(id=streamB.id).first()
                        cfb=ConfigB.objects.filter(id=stb.id_config.id).first()
                        #print("stream>",st,cf.Compression)
                        confB = confB + f"<h6>{stb.name}:</h6> "
                        confB = confB + f"Compression: {cfb.Compression} <br>"
                        confB = confB + f"Resolution: {cfb.resolution} <br>"
                        confB = confB + f"SmartCodec: {cfb.SmartCodec} <br>"
                        confB = confB + f"FPS: {cfb.FPS} <br>"
                        confB = confB + f"BitRateControl: {cfb.BitRateControl} <br>"
                        confB = confB + f"Quality: {cfb.Quality} <br>"
                        confB = confB + f"BitRate: {cfb.BitRate} <br>"
                        confB = confB + f"VideoEnable: {cfb.VideoEnable} <br>"
                        confB = confB + f"Language: {cfb.Language} <br>"
                        #confB = confB + f"CurrentTime: {cfb.CurrentTime} <br>"

                for channelA in channelsA:
                    #print(channel, channel.number)
                    confA = confA + f"<h5>Channel {channelA.number}: <h5>"
                    #print (channel.streams[0], type(channel.streams))
                    #stream = StreamB.objects.filter(channel.streams)
                    streamsA = channelA.streams.all().order_by('name')
                    for streamA in streamsA:
                        sta=Stream.objects.filter(id=streamA.id).first()
                        cfa=Config.objects.filter(id=sta.id_config.id).first()
                        #print("stream>",st,cf.Compression)
                        confA = confA + f"<h6>{sta.name}:</h6> "
                        confA = confA + f"Compression: {cfa.Compression} <br>"
                        confA = confA + f"Resolution: {cfa.resolution} <br>"
                        confA = confA + f"SmartCodec: {cfa.SmartCodec} <br>"
                        confA = confA + f"FPS: {cfa.FPS} <br>"
                        confA = confA + f"BitRateControl: {cfa.BitRateControl} <br>"
                        confA = confA + f"Quality: {cfa.Quality} <br>"
                        confA = confA + f"BitRate: {cfa.BitRate} <br>"
                        confA = confA + f"VideoEnable: {cfa.VideoEnable} <br>"
                        confA = confA + f"Language: {cfa.Language} <br>"
                        #confA = confA + f"CurrentTime: {cfa.CurrentTime} <br>"
                
                #Config B
                configs["idB"] = sitioB.sitio
                configs["ipB"] = sitioB.ip
                configs["statusB"] = sitioB.status
                configs["last_updateB"] = sitioB.last_update
                #print(conf)
                configs["confB"] = confB

                #Config A
                configs["idA"] = sitioA.sitio
                configs["ipA"] = sitioA.ip
                configs["statusA"] = sitioA.status
                configs["last_updateA"] = sitioA.last_update
                configs["confA"] = confA

                if confB == confA:
                    configs["diff"] = 0
                else: 
                    configs["diff"] = 1


                #dataB.append(configsB)
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

