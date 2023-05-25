# echo-server.py

import socket
import numpy as np
from lxml import objectify
import pandas as pd


string_input = '<carrierInformation><stationID>Station#13</stationID><carrierID>14</carrierID><timeDate>20/04/2023: 08:26:29</timeDate></carrierInformation>'

data = pd.read_csv('procssing_times_table.csv', sep=';')

processing_data = data.to_numpy()

print(processing_data[1,:])

class Carrier:
    def __init__(self, stationID, carrierID, timeDate):
        self.stationID = stationID
        self.carrierID = carrierID
        self.timeDate =  timeDate


    def proccessingTime(self):
        processing_time = 0
        match self.stationID:
            case "Station#13":
                return processing_time[1,1]
            
            case "Station#12":
                pass
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
            
            data_string = data.decode('utf-8')#str(data)

            print(data_string)

            carrier_object = objectify.fromstring(data_string)

            current_carrier = Carrier(carrier_object.stationID, carrier_object.carrierID, carrier_object.timeDate)
            current_carrier.info()
            processing_time = current_carrier.proccessingTime()

            print(processing_time)

            if not data:
                break
            conn.sendall(processing_time.to_bytes(2, 'little'))