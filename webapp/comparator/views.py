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
        return sitios


    def buscar_sitio_A(self):
        pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = []
        #Obtener configuraciones del sitio
        if 1:
            sitiosB=SitioB.objects.all().order_by('sitio')[:1000]
            for sitioB in sitiosB:
                sitioA=Sitio.objects.filter(sitio=sitioB.sitio).first()

                configs = {}
                confB = "0"
                confA = "0"
                #print(sitio.ip, sitio.status)
                channelsB=ChannelB.objects.filter(sitio=sitioB)
                channelsA=Channel.objects.filter(sitio=sitioA)
                #print(channels)
                for channelB in channelsB:
                    #print(channel, channel.number)
                    confB = confB + f"<h5>Channel {channelB.number}: <h5>"
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
                    confA = confA + f"<h5>Channel {channelA.number}: <h5>"
                    streamsA = channelA.streams.all().order_by('name')
                    for streamA in streamsA:
                        sta=Stream.objects.filter(id=streamA.id).first()
                        cfa=Config.objects.filter(id=sta.id_config.id).first()
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
                
                if confA == "0" and confB == "0":
                    configs["diff"] = "n/a"

                data.append(configs)
        context["configs"] = data
        print("Finished")
        return context