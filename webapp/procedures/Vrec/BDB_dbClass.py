#!/usr/bin/env python3
import mysql.connector
import pandas as pd
import logging
from   mysql.connector import errorcode
from   multiprocessing import Lock
from   datetime import datetime, timedelta

from django.core.mail import EmailMultiAlternatives
from django.conf import settings

ELIPGO_DDNSDomain = 'elipgodns.com'
DB_Host           = '10.200.3.80'
DB_Database       = 'bdb'
DB_User           = 'elipgo'
DB_Password       = '3l1pg0$123'

#
# Clase de la base de datos
#
class BDBDatabase:

    # Inicialización y conección a la Base de Datos
    def __init__(self, host = DB_Host, database = DB_Database, user = DB_User, password = DB_Password):
        #print("ElipgoDB Constructor(%s)" % (database))
        # Asigna variables de la clase
        self.host       = host
        self.database   = database
        self.user       = user
        self.password   = password
        self.lock       = Lock()
        self.connection = None

        

    def open_connection(self):
        try:
            self.connection = mysql.connector.connect(user      = self.user,
                                                      password  = self.password,
                                                      host      = self.host,
                                                      database  = self.database)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Algo esta mal con el Usuario y Password.")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("La base de datos no existe.")
            else:
                print(err)
    def close_connection(self):
        if self.connection:
            self.connection.close()


    def GetXVRIP(self):
        logging.info(f"GetXVRIP()")

        # Lectura de los registros de la table "direccionamiento" Sitios Fase 2
        self.lock.acquire()
        mycursor = self.connection.cursor()
        mycursor.execute("SELECT sucursal, xvr, xvr_port, xvr_user, xvr_password FROM vXVRIP where fase = 2")
        myresult = mycursor.fetchall()
        columns  = mycursor.description
        mycursor.close()
        self.lock.release()

        return(myresult)


    def GetVRecIP(self):
        logging.info(f"GetVFRecIP()")

        # Lectura de los registros de la table "direccionamiento" Sitios Fase 1
        self.lock.acquire()
        mycursor = self.connection.cursor()
        mycursor.execute("SELECT sucursal, xvr, xvr_port, xvr_user, xvr_password FROM vXVRIP where fase = 1")
        myresult = mycursor.fetchall()
        columns  = mycursor.description
        mycursor.close()
        self.lock.release()
        return(myresult)   




    def UpdateStatus(self, sucursal, status):
        logging.info(f"WriteStatus({sucursal}, '{status}')")

        queryStr = f"UPDATE sucursal SET status='{status}', lastUpdate='{datetime.now()}' WHERE sucursal = {sucursal}"

        try:
            self.lock.acquire()
            mycursor = self.connection.cursor()
            mycursor.execute(queryStr)
            self.connection.commit()
            mycursor.close()
        except:
            pass
        self.lock.release()


        # Actualiza el estatus del 
    def ReadCameraRecord(self, sucursal, camera):
        logging.info(f"ReadCameraRecord({sucursal},{camera})")

        queryStr = f"SELECT * FROM camara WHERE sucursal={sucursal} AND camara={camera}"
        try:
            self.lock.acquire()            
            mycursor = self.connection.cursor()
            mycursor.execute(queryStr)
            myresult = mycursor.fetchall()
            mycursor.close()
            self.lock.release()
            return myresult
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.lock.release()


    def GetSummary(self):
        logging.info(f"GetVFRecIP()")
        # Generar resumen de status de xvr
        offline = None
        self.lock.acquire()
        mycursor = self.connection.cursor()
        mycursor.execute("SELECT status,count(status) FROM camara group by status")
        myresult = mycursor.fetchall()
        summary_text = ""
        if myresult:
            camera_status = {}
            summary_text = summary_text + f"<br>[ Camaras con incidentes ] <br>"
            for result in myresult:   
                print(result[0],result[1])
                llave = result[0]
                valor = result[1]
                if llave=="Stopped":
                    llave="Camaras Detenidos"
                elif llave=="Starting":
                    llave="Camaras Reconectando"
                elif llave=="Error":
                    llave="Camaras Con Errores"
                elif llave=="RetryWait":
                    llave="Camaras Reintentando"
                elif llave=="Started":
                    llave="Camaras En linea"

                summary_text = summary_text + f"<br>{llave}:{valor}"
                camera_status[str(result[0])] = result[1]
        print(camera_status)

        mycursor.execute("SELECT status,count(status) FROM sucursal group by status")
        myresult = mycursor.fetchall()
        if myresult:
            sucursal_status = {}
            summary_text = summary_text + f"<br><br>[ Estado de sucursales ]<br>"
            for result in myresult:   
                print(result[0],result[1])
                llave = result[0]
                valor = result[1]
                summary_text = summary_text + f"<br>{llave}: {valor}"
                sucursal_status[str(result[0])] = result[1]
        print(sucursal_status)
        
        #mycursor.execute("SELECT * FROM camara_video_lost where last_update between '2023-03-11 00:00:00' and '2023-03-15 00:00:00' order by segmento_inicio desc")
        #myresult = mycursor.fetchall()
        #if myresult:
        #    sucursal_status = {}
        #    for result in myresult:   
        #        print(result[0],result[1])
        #        sucursal_status[str(result[0])] = result[1]
        #print(sucursal_status)
        
        queryStr =  f"select distinct video_lost.sucursal, sucursal.nombre,video_lost.camara,first_video, " \
                    f"last_video,segmento_inicio, segmento_fin," \
                    f"CONCAT(FLOOR(HOUR(TIMEDIFF(segmento_inicio, segmento_fin)) / 24), 'd , '," \
                    f"MOD(HOUR(TIMEDIFF(segmento_inicio, segmento_fin )), 24), 'h') as 'tiempo_segmento'," \
                    f"video_lost.last_update" \
                    f" FROM bdb.camara_video_lost video_lost " \
                    f" INNER JOIN bdb.camara camara ON video_lost.camara = camara.camara" \
                    f" INNER JOIN bdb.sucursal sucursal ON video_lost.sucursal = sucursal.sucursal" \
                    f" WHERE video_lost.segmento_inicio BETWEEN camara.first_video and camara.last_video" \
                    f" AND video_lost.segmento_fin BETWEEN camara.first_video and camara.last_video" \
        
        mycursor.execute(queryStr)
        myresult = mycursor.fetchall()
        columns  = mycursor.description
        headers = []
        for column in columns:
            headers.append(str(column[0]))
        print(headers)
        if myresult:
            pd.DataFrame(myresult).to_csv("camera_lost.csv",header=headers)

        today = datetime.now().date()
        yesterday = today.today() - timedelta(1)
        news =  f"select distinct video_lost.sucursal, sucursal.nombre,video_lost.camara,first_video, " \
                    f"last_video,segmento_inicio, segmento_fin," \
                    f"CONCAT(FLOOR(HOUR(TIMEDIFF(segmento_inicio, segmento_fin)) / 24), 'd , '," \
                    f"MOD(HOUR(TIMEDIFF(segmento_inicio, segmento_fin )), 24), 'h') as 'tiempo_segmento'," \
                    f"video_lost.last_update" \
                    f" FROM bdb.camara_video_lost video_lost " \
                    f" INNER JOIN bdb.camara camara ON video_lost.camara = camara.camara" \
                    f" INNER JOIN bdb.sucursal sucursal ON video_lost.sucursal = sucursal.sucursal" \
                    f" WHERE video_lost.segmento_inicio BETWEEN camara.first_video and camara.last_video and segmento_inicio between '{yesterday}' and '{today}' " \
                    f" AND video_lost.segmento_fin BETWEEN camara.first_video and camara.last_video" \
                    
        mycursor.execute(news)
        myresult = mycursor.fetchall()

        summary_text = summary_text + f"<br><br>[ Errores en la grabacion ] <br>"
        summary_text = summary_text + f"Segmentos de video perdidos nuevos: {len(myresult)}<br>"
        summary_text = summary_text + f"Sucursales con incidencias de video perdidos: 11 <br>"

        columns  = mycursor.description
        headers = []
        for column in columns:
            headers.append(str(column[0]))
        print(headers)
        if myresult:
            pd.DataFrame(myresult).to_csv("news.csv",header=headers)

        
        mycursor.execute("SELECT * FROM camara")
        myresult = mycursor.fetchall()
        columns  = mycursor.description
        headers = []
        for column in columns:
            headers.append(str(column[0]))
        print(headers)
        if myresult:
            pd.DataFrame(myresult).to_csv("summary.csv",header=headers)
                    
        #email_from=settings.EMAIL_HOST_USER
        #recipient_list=["roldan096@gmail.com"]
        #send_mail("TestMail", "Testing...", email_from, recipient_list)

        #email = EmailMessage(
        #    "Test",
        #    "msg1",
        #    settings.EMAIL_HOST_USER,
        #    ['roldan096@gmail.com']
        #    )
        #email.fail_silently = False
        #email.send()
        #self.send_email(["roldan096@gmail.com","jorge.pi@elipgo.com"],'summary.csv','news.csv', summary_text)
        self.send_email(["roldan096@gmail.com","jorge.pi@elipgo.com"],'summary.csv','camera_lost.csv','news.csv', summary_text)
        mycursor.close()
        self.lock.release()
        return(myresult)
    
    def send_email(self,receive_email_addr,file_path1,file_path2, file_path3, text_content):
        print ('************** Comience a generar mensajes *********************')
        asunto = '[ViVA-BANSEFI WatchDogRecordings] - Reporte de Grabadores'
        text_content = text_content
        html_content = f'<p> Resumen de incidentes . <br></ p> <p> {text_content} </ p> <br> <br>           \
                        Para mayor informacion sobre los incidentes reportados, revisar los archivos    \
                        adjuntos. <br>                                                                  \
                        ESTE MENSAJE ES GENERADO AUTOMATICAMENTE POR UNA HERRAMIENTA: NO LO             \
                        RESPONDA. '                                         
        from_email = settings.EMAIL_HOST_USER
        msg = EmailMultiAlternatives(asunto, text_content, from_email, receive_email_addr)
        msg.attach_alternative(html_content, "text/html")
        # enviar archivos adjuntos
        print ('******************** Enviar archivo adjunto ********************')
        msg.attach_file(file_path1)
        msg.attach_file(file_path2)
        msg.attach_file(file_path3)
        #msg.attach_file('files/media/myexcel.xlsx')
        msg.send()
        if msg.send():
                    print ('****************** enviado con éxito *********************')
        else:
                    print ('****************** Error de envío ************************')
    
    


    def UpdateCameraStatus(self, cameraInfo):
        logging.info(f"UpdateCameraStatus()")
        #print(cameraInfo)
        record = self.ReadCameraRecord(cameraInfo['sucursal'], cameraInfo['camara'])
        if record:
            #print("Existe, se debe actualizar")
            queryStr = f"UPDATE camara SET status='{cameraInfo['status']}', enable='{cameraInfo['enable']}' " \
                       f"WHERE sucursal={cameraInfo['sucursal']} and camara={cameraInfo['camara']}"

        #print(queryStr)
        try:
        #if 1:
            self.lock.acquire()
            mycursor = self.connection.cursor()
            mycursor.execute(queryStr)
            self.connection.commit()
            mycursor.close()
            self.lock.release()
        except:
        #else:
            pass
            self.lock.release()

    def TruncateTable(self, table):
        logging.info(f"TruncateTable()")
        queryStr = f"TRUNCATE table {table}" 
        try:
            self.lock.acquire()
            mycursor = self.connection.cursor()
            mycursor.execute(queryStr)
            self.connection.commit()
            mycursor.close()
            self.lock.release()
        except:
            pass
            self.lock.release()

    def UpdateCameraLost(self, cameraInfo, lost):
        logging.info(f"UpdateCameraLost()")
        #print(cameraInfo)
        if lost:
            for lost_segment in lost:
                logging.info(f"Lost(): {cameraInfo['sucursal'] , cameraInfo['camara'] ,lost_segment } ")
                if len(lost_segment) == 2:
                    queryStr = f"INSERT INTO camara_video_lost VALUES({cameraInfo['sucursal']}, {cameraInfo['camara']}, '{lost_segment[0]}'," \
                            f"'{lost_segment[1]}','{0}','{datetime.now()}')"

                    
                    #Buscar si existe el elemento
                    query1=f"SELECT * from camara_video_lost where sucursal={cameraInfo['sucursal']} and camara={cameraInfo['camara']} and segmento_inicio='{lost_segment[0]}'"
                    #print(queryStr)
                    myresult=None
                    try:
                        self.lock.acquire()
                        mycursor = self.connection.cursor()
                        mycursor.execute(query1)
                        myresult = mycursor.fetchall()
                        mycursor.close()
                        self.lock.release()
                    except:
                        pass

                    if myresult:
                        logging.info(f"YaExisteElRegistro(): {myresult} ")
                        logging.info(f"YaExisteElRegistro(): {myresult} ")
                    else:
                        logging.info(f"\n\n\nNoExisteElRegistro(): CreandoNuevoRegistro\n\n\n ")
                        #if len(lost_segment) == 2:
                        #    queryStr = f"INSERT INTO camara_video_lost VALUES({cameraInfo['sucursal']}, {cameraInfo['camara']}, '{lost_segment[0]}'," \
                        #            f"'{lost_segment[1]}','{0}', '2022-12-07 10:00:09')"
                        
                        #logging.info(f"Insertar:({queryStr})")

                        try:
                            self.lock.acquire()
                            mycursor = self.connection.cursor()
                            mycursor.execute(queryStr)
                            self.connection.commit()
                            mycursor.close()
                            self.lock.release()
                        except:
                            logging.warning(f"Error adding CameraLost()")
                            pass
                            self.lock.release()
        



    def UpdateCameraRecord(self, cameraInfo):
        logging.info(f"UpdateCameraRecord()")
        #print(cameraInfo)
        
        record = self.ReadCameraRecord(cameraInfo['sucursal'], cameraInfo['camara'])
        if not record:
            #print("No existe, se debe crear")
            queryStr = f"INSERT INTO camara VALUES({cameraInfo['sucursal']}, {cameraInfo['camara']}, '{cameraInfo['nombre']}'," \
                       f"'{cameraInfo['host']}',{cameraInfo['port']},'{cameraInfo['sdk']}','{cameraInfo['user']}',"             \
                       f"'{cameraInfo['password']}',{cameraInfo['fps']},'{cameraInfo['status']}','{cameraInfo['enable']}',"     \
                       f"'{cameraInfo['recycle_mode']}','{cameraInfo['recycle_status']}','{cameraInfo['firstDate']}',"          \
                       f"'{cameraInfo['lastDate']}','{datetime.now()}')"
        else:
            #print("Existe, se debe actualizar")
            queryStr = f"UPDATE camara SET status='{cameraInfo['status']}', enable='{cameraInfo['enable']}', " \
                       f"first_video='{cameraInfo['firstDate']}', last_video='{cameraInfo['lastDate']}' "      \
                       f"WHERE sucursal={cameraInfo['sucursal']} and camara={cameraInfo['camara']}"

        #print(queryStr)
        try:
            self.lock.acquire()
            mycursor = self.connection.cursor()
            mycursor.execute(queryStr)
            self.connection.commit()
            mycursor.close()
            self.lock.release()
        except:
            self.lock.release()


    def WriteLog(self, sucursal, estatus):
        logging.info(f"WriteLog({sucursal},'{estatus}')")

        queryStr = f"INSERT INTO process_log VALUES ({sucursal}, '{estatus}', '{datetime.now()}')"
        #print(queryStr)

        try:
            self.lock.acquire()
            mycursor = self.connection.cursor()
            mycursor.execute(queryStr)
            self.connection.commit()
            mycursor.close()
            self.lock.release()
        except mysql.connector.Error as err:
            print(f"WriteLog Exception: {err}")
            self.lock.release()
