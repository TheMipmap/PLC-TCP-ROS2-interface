
# echo-server.py

import socket
import numpy as np
from lxml import objectify
import pandas as pd

#importing ros dependencies
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

#data read into memory commented out for test
#data = pd.read_csv("procssing_times_table.csv",sep=";")
#processingTable = data.to_numpy()
#print(processingTable[13,13])



class Carrier:
    def __init__(self, stationID, carrierID, timeDate):
        self.stationID = stationID
        self.carrierID = carrierID
        self.timeDate =  timeDate


    def proccessingTime(self):
        processing_time = 0
        match self.stationID:
            case "Station#13":
                print("success")
                #print(f"sending {processingTable[self.carrierID-1,13]}")
                return 2.2
            
            case "ST_PLC_11":
                if self.carrierID > 8:
                    processing_time += 1
                return processing_time
            
            case _:
                return processing_time


    
    def info(self):
        print(f'Station ID: {self.stationID} \nCarrier ID: {self.carrierID} \nTime and date: {self.timeDate}')




class PlcPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period =  0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'StationID = ST_PLC_13, CarrierID = 14, TimeDate = 20/04/2023: 08:26:29'
       # msg.data = '<carrierInformation><stationID>ST_PLC_13</stationID><carrierID>14</carrierID><timeDate>20/04/2023: 08:26:29</timeDate></carrierInformation>'
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1







HOST = "10.0.2.15"  # Standard loopback interface address (localhost)
PORT = 50001  # Port to listen on (non-privileged ports are > 1023)
rclpy.init()
current_carrier = Carrier('',0,'')

#main part of the code

plcpublisher = PlcPublisher()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(141)
            data_str_raw = str(data)
            
            print(data_str_raw)
            #data_string = data.decode('utf-8')#str(data)
            try:
                data_string = data.decode('utf-8')#str(data)
                print(data_string)
            except:
                print("decode error")
                data_string = "error"

                
            print(data_string)
            try:
                carrier_object = objectify.fromstring(data_string)
            except:
                print("error in carier object")

            current_carrier.stationID = carrier_object.stationID
            current_carrier.carrierID = carrier_object.carrierID
            current_carrier.timeDate = carrier_object.timeDate

            current_carrier.info()
            processing_time = current_carrier.proccessingTime()


            print(processing_time)
            
            #plcpublisher.timer_callback(String('Station ID' + String(current_carrier.stationID)+ ' Carrier ID' + String(current_carrier.carrierID) + 'Time and date ' + current_carrier.timeDate))
            
            rclpy.spin_once(plcpublisher)


            if not data:
                break
            conn.sendall(processing_time.to_bytes(2, 'little'))
            data_string = ''
            
