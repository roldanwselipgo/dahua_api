#!/usr/bin/env python3
# Implementación de API de Dahua - Parsing
#
import re
from typing import MutableSet
from PIL    import Image

DEFXRES  = 2688
DEFYRES  = 1520
NORMAL   = 8192
FILEPATH = 'imagenes'


class DahuaParse:
    def __init__(self):
        self.seq       = 0
        self.bbData    = {}
        self.bbMapped  = []
        self.metadata  = []
        self.face      = False

    def Normalize(self, xRes = DEFXRES, yRes = DEFYRES):
        self.bbMapped.append(int(self.bbData['0'] * DEFXRES / NORMAL))
        self.bbMapped.append(int(self.bbData['1'] * DEFYRES / NORMAL))
        self.bbMapped.append(int(self.bbData['2'] * DEFXRES / NORMAL))
        self.bbMapped.append(int(self.bbData['3'] * DEFYRES / NORMAL))


    def Parse(self, line):
        #print("Parser:", line)

        reCType = re.search(r"Content-Type: \w+/\w+", line.decode('utf-8', 'ignore'))
        if reCType:
            cType   = reCType.group().split(" ")[1]
            reCLen  = re.search(r"Content-Length: \w+", line.decode('utf-8', 'ignore'))
            if reCLen:
                cLen = reCLen.group().split(" ")[1]

                # Proceso los Metadatos de la imagen, extrae las coordenadas del BoundingBox                
                if cType == 'text/plain':
                    splitted = str(line).split('\\r\\n')
                    for sValue in splitted:
                        if 'Events[0].' in sValue:
                            #print(sValue)
                            self.metadata.append(sValue)

                        bbSearch = re.search(r"Events\[\d\].Faces\[\d\].BoundingBox\[(\d)\]=(\d+)", sValue)    
                        if bbSearch:
                            self.bbData[bbSearch.group(1)] = int(bbSearch.group(2))

                # Procesa y guarda la imagen recibida en el mensaje
                if cType == 'image/jpeg':
                    
                    # Escribe archivo con MetaData
                    fileName = '%s/Data%d.txt' % (FILEPATH, self.seq)
                    with open(fileName, "wt") as f:
                        for data in self.metadata:
                            #print(">>>", data)
                            f.write(data)
                            f.write('\r\n')
                            if '.Image.' in data:
                                self.face = True
                                print(data)
                    f.close()
                    
                    self.Normalize()
                    print("Boundary: ", self.bbData)
                    print("Mapped:   ", self.bbMapped)

                    #pos = str(line).find("Content-Length:")
                    #print("POS1: ", pos)
                    pos1 = line.find(b"\xff")
                    #print("POS2: ", pos1)

                    image = bytearray(line[pos1:int(cLen)])
                    if self.face:
                        fileName = '%s/Face%d.jpg'   % (FILEPATH, self.seq)
                    else:
                        fileName = '%s/Imagen%d.jpg' % (FILEPATH, self.seq)

                    with open(fileName, 'wb') as f:
                        f.write(image)
                    f.close()

                    # Corta la Imagen
                    #original = Image.open(fileName)
                    #cropped = original.crop(self.bbMapped)
                    #cropped.save(fileCropped)
                    
                    self.metadata = []
                    self.bbMapped = []
                    self.face     = False
                    self.seq += 1            
