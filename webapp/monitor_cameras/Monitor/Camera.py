import os,sys,time
from .Variable import Variable
from .Comunicacion import Comunicacion
from .Interfaz import Interfaz

class Camera(Variable):
    """
    Clase utulizada para definir un dispositivo camara y sus metodos basados en el manual DAHUA_HTTP_API_V2.841
    """
    HABILITAR = b'\xAC'
    DESHABILITAR = b'\xAB'

    def __init__(self, tag, nombre, descripcion,**kwargs):
        Variable.__init__ (self, tag = tag, nombre = nombre, descripcion = descripcion)

        self.establecer_nombre(nombre)

        self.equipoInicializado = False

        self.variables = []

        for i in range(80):
            self.variables.append(Variable("X_{:02d}".format(i), "", ""))

        self.variables[0]=Variable("X_00", "Fabricante", "Nombre del fabricante")
        self.variables[1]=Variable("X_01", "Modelo", "")
        self.variables[2]=Variable("X_02", "Número de Serie", "Número de ser")
        self.variables[3]=Variable("X_03", "Versión de Software", "")
        self.variables[4]=Variable("X_04", "", "")
        self.variables[5]=Variable("X_05", "Estatus", "")
        self.variables[6]=Variable("X_06", "", "")
        self.variables[7]=Variable("X_07", "", "")
        
        self.variables[8]=Variable("X_08", "", "")
        self.variables[9]=Variable("X_09", "", "")
        self.variables[10]=Variable("X_10", "", "")
        self.variables[11]=Variable("X_11", "", "")
        self.variables[12]=Variable("X_12", "", "")
        self.variables[13]=Variable("X_13", "", "")
        self.variables[14]=Variable("X_14", "", "")
        self.variables[15]=Variable("X_15", "", "")
        self.variables[16]=Variable("X_16", "", "")
        self.variables[17]=Variable("X_17", "", "")
        self.variables[18]=Variable("X_18", "", "")
        self.variables[19]=Variable("X_19", "", "")
        self.variables[20]=Variable("X_20", "", "")
        self.variables[21]=Variable("X_21", "", "")
        self.variables[22]=Variable("X_22", "", "")
        self.variables[23]=Variable("X_23", "", "")
        self.variables[24]=Variable("X_24", "", "")
        self.variables[25]=Variable("X_25", "", "")
        self.variables[26]=Variable("X_26", "", "")
        self.variables[27]=Variable("X_27", "", "")
        self.variables[28]=Variable("X_28", "", "")
        self.variables[29]=Variable("X_29", "", "")
        self.variables[30]=Variable("X_30", "", "")


        self.configurarDispositivo (**kwargs)
        self.actualizar()

        print ("\n->Se ha configurado el {}".format(self))

    def establecerPuerto(self, puerto):
        self.puerto = puerto

    def establecerComunicacion (self, comunicacion):
        self.comunicacion = comunicacion
    
    def establecer_nombre (self, nombre):
        self.nombre = nombre

        
    def configurarDispositivo (self, *args, **kwargs):
        #print ("Desde configurarDispositivo", args , kwargs)
        for key, value in kwargs.items():
            #print ("Imprimiendo el valor en modificar configuracion", key, value)
            if key == "valor":
                self.variables[3].establecerValor(value)
            if key == "direccion":
                self.variables[0].establecerValor(value)

    def obtener_datos_generales(self):
        metodo =  "configManager.cgi"
        parametros = { "action" : "getConfig" , "name" : "General"}
        a = self.comunicacion.crearInstruccionHttp(Comunicacion.PROCESO, Comunicacion.HTTP_DATOS_DAHUA, metodo, parametros)
        result = self.puerto.enviar(Interfaz.METODO_GET,a)
        if result:
            result = self.result_to_json(result.text)
        return result
    
    def obtener_current_time(self):
        metodo =  "global.cgi"
        parametros = { "action" : "getCurrentTime"}
        a = self.comunicacion.crearInstruccionHttp(Comunicacion.PROCESO, Comunicacion.HTTP_DATOS_DAHUA, metodo, parametros)
        result = self.puerto.enviar(Interfaz.METODO_GET,a)
        if result:
            result = self.result_to_json(result.text)
        return result

    def obtener_locales_config(self):
        metodo =  "configManager.cgi"
        parametros = { "action" : "getConfig","name":"Locales"}
        a = self.comunicacion.crearInstruccionHttp(Comunicacion.PROCESO, Comunicacion.HTTP_DATOS_DAHUA, metodo, parametros)
        result = self.puerto.enviar(Interfaz.METODO_GET,a)
        if result:
            result = self.result_to_json(result.text)
        return result
    
    def obtener_device_type(self):
        metodo =  "magicBox.cgi"
        parametros = { "action" : "getDeviceType"}
        a = self.comunicacion.crearInstruccionHttp(Comunicacion.PROCESO, Comunicacion.HTTP_DATOS_DAHUA, metodo, parametros)
        result = self.puerto.enviar(Interfaz.METODO_GET,a)
        if result:
            result = self.result_to_json(result.text)
        return result

    def obtener_machine_name(self):
        metodo =  "magicBox.cgi"
        parametros = { "action" : "getMachineName"}
        a = self.comunicacion.crearInstruccionHttp(Comunicacion.PROCESO, Comunicacion.HTTP_DATOS_DAHUA, metodo, parametros)
        result = self.puerto.enviar(Interfaz.METODO_GET,a)
        #if result:
        #    result = self.result_to_json(result.text)
        self.variables[2].establecerDescripcion(result.text)
        return result

    def obtener_serial_no(self):
        metodo =  "magicBox.cgi"
        parametros = { "action" : "getSerialNo"}
        a = self.comunicacion.crearInstruccionHttp(Comunicacion.PROCESO, Comunicacion.HTTP_DATOS_DAHUA, metodo, parametros)
        result = self.puerto.enviar(Interfaz.METODO_GET,a)
        if result:
            result = self.result_to_json(result.text)
            self.variables[2].establecerDescripcion(result.get('sn'))
            result = result.get('sn')
        return result
    
    def obtener_motion_settings(self):
        metodo =  "configManager.cgi"
        parametros = { "action" : "getConfig","name":"MotionDetect"}
        a = self.comunicacion.crearInstruccionHttp(Comunicacion.PROCESO, Comunicacion.HTTP_DATOS_DAHUA, metodo, parametros)
        result = self.puerto.enviar(Interfaz.METODO_GET,a)
        if result:
            result = self.result_to_json(result.text)
        return result
    
    def actualizar_motion_settings(self, estado=None,**kwargs):
        metodo =  "configManager.cgi"
        parametros = { "action" : "setConfig","MotionDetect[0].Enable":estado}
        a = self.comunicacion.crearInstruccionHttp(Comunicacion.PROCESO, Comunicacion.HTTP_DATOS_DAHUA, metodo, parametros)
        result = self.puerto.enviar(Interfaz.METODO_GET,a)
        #if result:
        #    result = self.result_to_json(result.text)
        return result
    
    def obtener_snapshot(self):
        metodo =  "snapshot.cgi"
        parametros = { "channel" : "1"}
        a = self.comunicacion.crearInstruccionHttp(Comunicacion.PROCESO, Comunicacion.HTTP_DATOS_DAHUA, metodo, parametros)
        result = self.puerto.enviar(Interfaz.METODO_GET,a)
        #if result:
        #    result = self.result_to_json(result.text)
        return result


    def result_to_json(self, datos):
        datos_json = datos.replace("\r\n",',')
        datos_json = datos_json[:-1]
        result = dict((a.strip(), str(b.strip()))  
                     for a, b in (element.split('=')  
                                  for element in datos_json.split(',')))
        return result
        

    def obtenerNombre(self):
        return self.nombre

    def __str__ (self):
        return "%s " %(self.obtenerNombre())
    

def main ():
    puerto = Interfaz("api")
    puerto.modificarConfiguracion(
                                dispositivo = Interfaz.CAMARA_DAHUA, 
                                protocolo = 'http', 
                                servidor = 'elipgomexico.ddns.net', 
                                puerto = '1938', 
                                usuario = 'test', 
                                password = 'test$2022'
                                )
    comunicacion = Comunicacion ()
    puerto.inicializar()
    
    # Se crea y se configura el dispositivo
    camera1 = Camera("Camera 1", "CAM-001", "En camara")
    camera1.establecerPuerto (puerto)
    camera1.establecerComunicacion (comunicacion)
    camera1.obtener_datos_generales()
    camera1.obtener_current_time()
    camera1.obtener_locales_config()
    

if __name__ == "__main__":
    main()