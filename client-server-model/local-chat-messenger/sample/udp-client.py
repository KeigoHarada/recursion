import socket
import sys
import os
socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
server_address = '/tmp/chat_socket'
client_address = '/tmp/chat_socket_client'

try:
    os.unlink(client_address)
except FileNotFoundError:
    pass

socket.bind(client_address)


try:
    message = b'Hello, Server!'
    socket.sendto(message, server_address)
    print(f"Sent message to {server_address}")
    response, server_address = socket.recvfrom(1024)
    print(f"Received response from {server_address}: {response.decode('utf-8')}")
finally:
    print("Closing socket")
    socket.close()
