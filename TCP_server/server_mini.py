# echo-server.py

import socket
import xml.sax
import numpy as np
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)


#Class for handling the XML file
class CarrierHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.CurrentData = ""
        self.stationID = ""
        self.carrierID = 0
        self.timeDate = ""

    # Call when an element starts
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        # if tag == "RotationalMatrix":
        #     print ("*****Rotational Values*****")
        # elif tag == "TranslationalVector":
        #     print("*****Translational Values*****")

    # Call when an elements ends
    def endElement(self, tag):
        self.CurrentData = ""

    # Call when a character is read
    def characters(self, content):
        if self.CurrentData == "stationID":
            self.stationID = str(content)
        elif self.CurrentData == "CarrierID":
            self.carrierID = int(content)
        elif self.CurrentData == "timeDate":
            self.timeDate = str(content)


class Carrier:
    def __init__(self, stationID, carrierID, timeDate):
        self.stationID = stationID
        self.carrierID = carrierID
        self.timeDate =  timeDate


    def proccessingTime(self):
        processing_time = 0
        match self.stationID:
            case "ST_PLC_13":
                if self.carrierID > 8:
                    processing_time = 5
                else:
                    processing_time = 2
                return processing_time
            
            case "ST_PLC_11":
                if self.carrierID > 8:
                    processing_time += 1
                return processing_time
            
            case _:
                return processing_time


    
    def info(self):
        print(f'Station ID: {self.stationID} \nCarrier ID: {self.carrierID} \nTime and date: {self.timeDate}')



HOST = "172.20.10.2"  # Standard loopback interface address (localhost)
PORT = 20001  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(16384)

            # create an XMLReader
            parser = xml.sax.make_parser()
            # turn off namepsaces
            parser.setFeature(xml.sax.handler.feature_namespaces, 0)

            # override the default ContextHandler
            Handler = CarrierHandler()
            parser.setContentHandler(Handler)

            parser.parseString(data.decode("utf-8"), Handler)
            #parser.parse("matrix.xml")
            current_carrier = Carrier(Handler.stationID, Handler.carrierID, Handler.timeDate)
            
            processing_time = current_carrier.proccessingTime()

            print(processing_time)

            if not data:
                break
            conn.sendall(processing_time.to_bytes(2, 'little'))