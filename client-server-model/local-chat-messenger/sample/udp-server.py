import os
import socket

socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
server_address = '/tmp/chat_socket'

try:
    os.unlink(server_address)
except FileNotFoundError:
    pass

print(f"Server is running on {server_address}")

socket.bind(server_address)

while True:
    data, client_address = socket.recvfrom(1024)
    if data:
        print(f"Received message: {data.decode('utf-8')}")
        response = 'Processing' + data.decode('utf-8')
        socket.sendto(response.encode('utf-8'), client_address)
        