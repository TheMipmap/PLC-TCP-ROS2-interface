# echo-client.py

import socket

HOST = "172.20.10.2"  # The server's hostname or IP address
PORT = 20001  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'<carrierInformation><stationID>ST_PLC_11</stationID><carrierID>14</carrierID><timeDate>20/04/2023: 08:26:29</timeDate></carrierInformation>')
    data = s.recv(16384)

print(f"Received {data!r}")