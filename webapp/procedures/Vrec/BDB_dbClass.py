#!/usr/bin/env python3
import mysql.connector
import pandas as pd
import logging
from   mysql.connector import errorcode
from   multiprocessing import Lock
from   datetime import datetime, timedelta
import collections

#EmailMessage
import smtplib
import ssl
from email.message import EmailMessage
import mimetypes
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



    def UpdateStatusNoIp(self, sucursal, status):
        logging.info(f"WriteStatus({sucursal}, '{status}')")
        queryStr = f"UPDATE devices.dvrDevices SET status={status}, lastStatus='{datetime.now()}' WHERE hostname= '{sucursal}'"
        try:
            self.lock.acquire()
            mycursor = self.connection.cursor()
            mycursor.execute(queryStr)
            self.connection.commit()
            mycursor.close()
        except:
            pass
        self.lock.release()

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


    def GetSummaryDahua(self):
        logging.info(f"GetVFRecIP()")
        # Generar resumen de status de xvr
        self.lock.acquire()
        mycursor = self.connection.cursor()
        mycursor.execute("SELECT distinct sucursal,channel FROM bdb.segmento_video")
        myresult = mycursor.fetchall()
        mycursor.execute("SELECT distinct sucursal FROM bdb.segmento_video")
        sucursales = mycursor.fetchall()
        summary_text = ""
        if myresult:
            camera_status = {}
            summary_text = summary_text + f"\n\n[ Estado de Grabacion ]"
            summary_text = summary_text + f"\n Grabando: {len(myresult)} camaras de {len(sucursales)} sucursales disponibles "

        mycursor.execute("SELECT status,count(status) FROM sucursal where fase!=1 group by status")
        myresult = mycursor.fetchall()
        if myresult:
            sucursal_status = {}
            summary_text = summary_text + f"\n\n[ Estado de sucursales ]"
            for result in myresult:   
                print(result[0],result[1])
                llave = result[0]
                valor = result[1]
                summary_text = summary_text + f"\n{llave}: {valor}"
                sucursal_status[str(result[0])] = result[1]
                
        print(sucursal_status)

        queryStr = "SELECT segmento_video2.sucursal ,sucursal.nombre, segmento_video2.ip," \
                "segmento_video2.channel, segmento_video2.starttime, segmento_video2.endtime, segmento_video2.diff  " \
                " FROM bdb.sucursal sucursal INNER JOIN bdb.segmento_video2 segmento_video2 ON sucursal.sucursal = segmento_video2.sucursal"

        mycursor.execute(queryStr)
        myresult = mycursor.fetchall()

        summary_text = summary_text + f"\n\n[ Errores en la grabacion ]"
        summary_text = summary_text + f"\nSegmentos de video perdidos nuevos: {len(myresult)}"
        #summary_text = summary_text + f"\nSucursales con incidencias de video perdidos: 11 "

        summary_text = summary_text + "\n\n\n\nPara mayor informacion sobre los incidentes reportados, revisar los archivos adjuntos."
        summary_text = summary_text + "\n\nESTE MENSAJE ES GENERADO AUTOMATICAMENTE POR UNA HERRAMIENTA: NO LORESPONDA."

        columns  = mycursor.description
        headers = []
        for column in columns:
            headers.append(str(column[0]))
        print(headers)
        if myresult:
            pd.DataFrame(myresult).to_csv("news_f2.csv",header=headers)

        #self.send_email(["roldan096@gmail.com","jorge.pi@elipgo.com"],'summary.csv','camera_lost.csv','news.csv', summary_text)
        self.send_email(["roldan096@gmail.com","jorge.pi@elipgo.com"],'news_f2.csv','news_f2.csv','news_f2.csv', summary_text)
        mycursor.close()
        self.lock.release()
        return(myresult)


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
            summary_text = summary_text + f"\n\n[ Camaras con incidentes ]"
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

                summary_text = summary_text + f"\n{llave}:{valor}"
                camera_status[str(result[0])] = result[1]
        print(camera_status)

        mycursor.execute("SELECT status,count(status) FROM sucursal where fase=1 group by status")
        myresult = mycursor.fetchall()
        if myresult:
            sucursal_status = {}
            summary_text = summary_text + f"\n\n[ Estado de sucursales ]"
            for result in myresult:   
                print(result[0],result[1])
                llave = result[0]
                valor = result[1]
                summary_text = summary_text + f"\n{llave}: {valor}"
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
        counter = collections.Counter(myresult)
        print("Counter sucursales vlost:", counter)

        summary_text = summary_text + f"\n\n[ Errores en la grabacion ]"
        summary_text = summary_text + f"\nSegmentos de video perdidos nuevos: {len(myresult)}"
        #summary_text = summary_text + f"\nSucursales con incidencias de video perdidos: 11 "

        summary_text = summary_text + "\n\n\n\nPara mayor informacion sobre los incidentes reportados, revisar los archivos adjuntos."
        summary_text = summary_text + "\n\nESTE MENSAJE ES GENERADO AUTOMATICAMENTE POR UNA HERRAMIENTA: NO LORESPONDA."

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
        #self.send_email(["roldan096@gmail.com"],'summary.csv','camera_lost.csv','news.csv', summary_text)
        self.send_email(["roldan096@gmail.com","brian.pichardo@viva-telmex.com","jorge.pi@elipgo.com"],'summary.csv','camera_lost.csv','news.csv', summary_text)
        
        mycursor.close()
        self.lock.release()
        return(myresult)
    
    def attach_file_to_email(self,email, filename):
        """Attach a file identified by filename, to an email message"""
        with open(filename, 'rb') as fp:
            file_data = fp.read()
            maintype, _, subtype = (mimetypes.guess_type(filename)[0] or 'application/octet-stream').partition("/")
            email.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=filename)

    def send_email(self,receive_email_addr,file_path1,file_path2, file_path3, text_content):
        """print ('************** Comience a generar mensajes *********************')
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
        """
        
        # Define email sender and receiver
        email_sender = 'rodrigo.roldan@elipgo.com'
        email_password = 'gnyjylabspgvakia'
        email_receiver = receive_email_addr

        # Set the subject and body of the email
        subject = '[ViVA-BANSEFI WatchDogRecordings] - Reporte de Grabadores'
        body = text_content

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)
        
        self.attach_file_to_email(em, file_path1)
        self.attach_file_to_email(em, file_path2)
        self.attach_file_to_email(em, file_path3)

        # Add SSL (layer of security)
        context = ssl.create_default_context()

        # Log in and send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
    
    


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
