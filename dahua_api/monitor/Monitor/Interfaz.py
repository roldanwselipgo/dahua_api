# Create your tests here.
from datetime import datetime, date, time, timedelta
import os,sys,time
import requests,json
from requests.auth import HTTPDigestAuth

class Interfaz:
    """
    Clase utulizada para consumir un api con python 
    """
    ADMINISTRACION = 1
    PROCESO = 2
    INTERFAZ = 3
    CODIGOS_EXITOSOS = (200,201,206)
    METODO_GET = 'GET'
    METODO_POST = 'POST'
    CAMARA_DAHUA = 1
    def __init__(self, nombre):
        self.dispositivo = 1
        self.url = ''
        self.protocolo = None
        self.servidor = None
        self.usuario = None
        self.password = None
        self.ruta = ''
        self.encabezados = ''
        self.auth = ''
        self.metodo = None
        self.datos = None
        self.status_code = None
        self.response = None
    
    def inicializar(self):
        self.establecer_conexion()
    
    def modificarConfiguracion (self, **kwargs):
        for key, value in kwargs.items():

            #print ("Imprimiendo el valor en modificar configuracion", key, value)
            if key == "dispositivo":
                self.dispositivo = value

            if key == "protocolo":
                self.protocolo = value
            
            if key == "puerto":
                self.puerto = value

            if key == "servidor":
                self.servidor = value

            if key == "usuario":
                
                self.usuario = value
                
            if key == "password":
                self.password = value
             
            
    
    def establecer_conexion(self):
        if self.usuario and self.password:
            self.establecer_auth(self.usuario,self.password)
            print("Se establecio la autenticacion")

    def obtener_url(self,url):
        return self.url
    def obtener_encabezado(self):
        return self.encabezado
    def obtener_metodo(self,metodo):
        return self.metodo

    def construir_url(self):
        """ construye la con los datos actuales """
        self.url =  "{}://{}:{}".format(self.protocolo,self.servidor,self.puerto)
        return self.url
    

    def establecer_auth(self,usuario,password):        
        self.auth = HTTPDigestAuth(usuario, password)

    def establecer_encabezado(self,encabezado):
        self.encabezados = encabezado
    def establecer_metodo(self,metodo):
        self.metodo = metodo

        
    def enviar(self, metodo, parametros = None, mensaje = None):
        err = 0
        url = self.construir_url()
        if parametros:
            url = url + parametros

        try:
             

            if metodo == 'GET':
                url = url.split('?')
                print("Accediendo a : ", url)
                self.establecer_encabezado({'Content-Type': 'application/x-www-form-urlencoded'})
                response = requests.get(
                                        url=url[0],
                                        params =url[1],
                                        headers=self.encabezados,
                                        auth=self.auth,
                                        verify=False, 
                                        stream=True
                )
                
                if response.status_code not in self.CODIGOS_EXITOSOS:
                    err = 1
                else:
                    return response
                
            elif metodo == 'POST':
                response = requests.post(
                                        self.url, data=json.dumps(self.datos),
                                        headers=self.encabezado
                )
                if response.status_code not in self.CODIGOS_EXITOSOS:
                    err = 1
                
            elif metodo == 'PUT':
                response = requests.put(
                self.url, data=json.dumps(self.datos),
                headers=self.encabezado
                )
                if response.status_code not in self.CODIGOS_EXITOSOS:
                    err = 1
            elif metodo == 'DELETE':
                pass

            self.status_code = response.status_code
            self.response = response.json()

            if err:
                return -1
                print("Ocurrio un error:",response.status_code)
            else: 
                return self.response
        except:
            self.response = 0
            text = "[{}] [Error3] Vista sin respuesta".format(time.strftime("%Y-%m-%d %H:%M:%S"))
            #print(colored(text, 'red'))
            print(text)

    
    def validar_datos(self,datos):
        if datos:
            return 1
        else: 
            return 0



    

def main():
    
    ### ------------------------------- Declarar la interfaz
    interfaz_api = Interfaz()
    print("#-------------------Prueba Camara: ")
    body = ""
    #metodo = "GET"
    interfaz_api.establecer_protocolo('http')
    interfaz_api.establecer_servidor('elipgomexico.ddns.net:1938')
    interfaz_api.establecer_abs_path('cgi-bin')
    interfaz_api.construir_url()
    interfaz_api.establecer_metodo('GET')
    interfaz_api.establecer_auth(HTTPDigestAuth('test', 'test$2022'))
    #interfaz_api.establecer_encabezado({'Content-Type': 'application/json'})
    interfaz_api.establecer_query('configManager.cgi?action=getConfig&name=General')
    #interfaz_api.establecer_query('snapshot.cgi?channel=1')
    response = interfaz_api.enviar(Interfaz.PROCESO,body)
    print(response.text)
    
if __name__ == "__main__":
    main()

