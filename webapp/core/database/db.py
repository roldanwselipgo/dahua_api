#!/usr/bin/env python3
import mysql.connector
from mysql.connector import Error

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


#
# Clase de la base de datos
#
class DB:

    # Inicialización y conección a la Base de Datos
    def __init__(self, host, database, user, password):
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
            #print(self.connection)
        except:
            print(f"Sin conexion a {self.database}")
            self.connection = None
        """except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Algo esta mal con el Usuario y Password.")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("La base de datos no existe.")
            else:
                print(err)"""

            
    def close_connection(self):
        if self.connection:
            self.connection.close()


    def query(self, query):
        logging.info(f"query()")
        try:
            self.lock.acquire()
            mycursor = self.connection.cursor()
            mycursor.execute(query)
            myresult = mycursor.fetchall()
            mycursor.close()
            self.lock.release()
            return myresult
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.lock.release()
            return 0

    def query_one(self, query):
        logging.info(f"query()")
        try:
            self.lock.acquire()
            mycursor = self.connection.cursor()
            mycursor.execute(query)
            myresult = mycursor.fetchone()
            mycursor.close()
            self.lock.release()
            return myresult
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.lock.release()
            return 0
    
    def execute(self, query):
        logging.info(f"insert_or_update()")
        # Lectura de los registros de la table "direccionamiento" Sitios Fase 2
        try:
            self.lock.acquire()            
            mycursor = self.connection.cursor()
            mycursor.execute(query)
            self.connection.commit()
            mycursor.close()
            self.lock.release()
            return 1
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.lock.release()
            return -1



    