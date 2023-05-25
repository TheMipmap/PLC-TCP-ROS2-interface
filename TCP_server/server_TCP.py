# echo-server.py

import socket
import numpy as np
from lxml import objectify
import pandas as pd

data = pd.read_csv("/Users/mortenstephansen/Desktop/Projects/PLC-TCP-ROS2-interface/TCP_server/procssing_times_table.csv",sep=";")
processingTable = data.to_numpy()
#print(processingTable[13,13])



class Carrier:
    def __init__(self, stationID, carrierID, timeDate):
        self.stationID = stationID
        self.carrierID = carrierID
        self.timeDate =  timeDate


    def proccessingTime(self):
        processing_time = 0
        match self.stationID:
            case "ST_PLC_13":
                #print(f"Sending {processingTable[self.carrierID-1,13]}")
                return processingTable[self.carrierID-1, 13]
            case "ST_PLC_12":
                return processingTable[self.carrierID-1, 12]

            case "ST_PLC_11":
                return processingTable[self.carrierID-1, 11]
            
            case _:
                return processing_time


    
    def info(self):
        print(f'Station ID: {self.stationID} \nCarrier ID: {self.carrierID} \nTime and date: {self.timeDate}')



HOST = "172.20.10.2" #172.20.66.38"  # Standard loopback interface address (localhost)
PORT = 20001  # Port to listen on (non-privileged ports are > 1023)


# The next line opens a socket with the IPv4 address family (socket.AF_INET) using the TCP protocol (socket.SOCK_STREAM)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(141)

            try:
                data_string = data.decode('utf-8')
                print(data_string)
            except:
                print("decode error")
                data_string = "error"

                
            try:
                carrier_object = objectify.fromstring(data_string)
            except:
                print("error in carier object")


            current_carrier = Carrier(carrier_object.stationID, carrier_object.carrierID, carrier_object.timeDate)

            current_carrier.info()
            processing_time = current_carrier.proccessingTime()

            print(processing_time)

            if not data:
                break
            conn.sendall(processing_time.to_bytes(2, 'little'))
            data_string = ''
            