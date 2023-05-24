import socket
from lxml import objectify

HOST = "172.20.66.39"  # Standard loopback interface address (localhost)
PORT = 11381  # Port to listen on (non-privileged ports are > 1023)



def bytestream_splicing(bytestream,print=False):
    # Find the index of the null byte that separates the XML message from the additional bytes
    null_byte_index = bytestream.find(b"</plcData>") + 10

    # Slice the byte string to extract the XML message
    xml_message = bytestream[:null_byte_index]

    # Decode the XML message to a string
    xml_string = xml_message.decode('utf-8')

    # Print the resulting string
    if print == True:
        print(xml_string)
    
    # Return the resulting string
    return xml_string



def main():
    print("Server started...")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data_message = conn.recv(128)

                # Cut null bytes off
                xml_string = bytestream_splicing(data_message)
                
                # Parse string
                data_object = objectify.fromstring(xml_string)
                print(data_object.stationID,data_object.carrierID,data_object.date)

                if not data_message:
                    break