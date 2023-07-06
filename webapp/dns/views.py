from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpResponseRedirect

from datetime import datetime
import os
import shutil
from .models import DNS
from .forms import DNSForm
import requests,json
from requests.auth import HTTPDigestAuth

from core.dahuaClasses.dahua_config import Config as Conf
from core.dahuaClasses.dahua_class import Dahua

from django.contrib import messages

from core.database.db import DB
# Create your views here.

class DNSDetailView(DetailView):
    """ Vista encargada de detallar el dispositivo seleccionado """
    model = DNS
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DNSListView(ListView):
    """ Vista encargada de listar los dispositivos registrados """
    model = DNS
    success_url = reverse_lazy('dns:dnss')
    def post(self, request, *args, **kwargs):
        #form = self.form_class(request.POST)
        #if form.is_valid():
        if self.request.method == "POST":
            # <process form cleaned data>
            if 1:
                print("Post method")
                hostname = self.request.POST.get("hostname","")
                ip = self.request.POST.get("ip","")
                DNS.objects.create(hostname=hostname, ip=ip)
                print(hostname, ip, type(ip))
                #df = pd.read_csv(file)
                #print(df.values[0])
        return HttpResponseRedirect(reverse_lazy('dns:dnss'))
                
        
    def get_queryset(self):
        dns=DNS.objects.all()
        return dns

class DNSCreateView(CreateView):
    model = DNS
    form_class = DNSForm
    success_url = reverse_lazy('dns:dnss')
    def form_valid(self, form):
        # Realizar acciones adicionales después de enviar el formulario correctamente
        # Por ejemplo, guardar datos adicionales, enviar notificaciones, etc.
        # Puedes acceder a los datos del formulario utilizando 'form.cleaned_data'
        # Ejemplo de acción: Imprimir los datos del formulario en la consola
        hostname = form.cleaned_data['hostname']
        ip = form.cleaned_data['ip']
        db = DB(host='10.200.3.80' , database='devices', user='elipgo', password='3l1pg0$123')
        db.open_connection()
        result = db.query(f"select * from devices.OracleDns where hostname='{hostname}'")
        if not result:
            db.execute(f"insert into devices.OracleDns (hostname,ipNoIpActual,status) values ('{hostname}','{ip}','new')")
        db.close_connection()

        # Llamar al método form_valid() de la clase padre para guardar los datos del formulario
        return super().form_valid(form)
    

class DNSUpdateView(UpdateView):
    model = DNS
    form_class = DNSForm
    template_name_suffix = '_update_form'
    def get_success_url(self):
        return reverse_lazy('dns:update', args=[self.object.id]) + '?ok'
    
    def form_valid(self, form):
        # Realizar acciones adicionales después de enviar el formulario correctamente
        # Por ejemplo, guardar datos adicionales, enviar notificaciones, etc.
        # Puedes acceder a los datos del formulario utilizando 'form.cleaned_data'
        # Ejemplo de acción: Imprimir los datos del formulario en la consola
        hostname = form.cleaned_data['hostname']
        ip = form.cleaned_data['ip']
        try:
            db = DB(host='10.200.3.80' , database='devices', user='elipgo', password='3l1pg0$123')
            db.open_connection()
            if db.connection.is_connected():
                result = db.query(f"select * from devices.OracleDns where hostname='{hostname}'")
                if result:
                    result = db.execute(f"update devices.OracleDns set ipNoIpActual='{ip}' where hostname='{hostname}'")
                else:
                    print("404 not found")
                print(form.cleaned_data)
                db.close_connection()
            else: 
                print("No connectio to DB")
                return 0
        except:
            print("Sin conexion a DB")

        # Llamar al método form_valid() de la clase padre para guardar los datos del formulario
        return super().form_valid(form)

class DNSDeleteView(DeleteView):
    model = DNS
    success_url = reverse_lazy('dns:dnss')

