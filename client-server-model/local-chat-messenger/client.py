import socket
import os

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)

socket.connect(server_address)
socket.settimeout(1)
while True:
    try:
        message = input("Enter a message: ")
        socket.sendall(message.encode('utf-8'))
        while True:
            try:
                response = socket.recv(1024)
                print(f"Received response: {response.decode('utf-8')}")
            except:
                print("No response received from server")
                break
    except:
        print("Connection closed")
        break

socket.close()


