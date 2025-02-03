import os
import socket

socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server_address = '/tmp/chat_socket'

try:
    os.unlink(server_address)
except FileNotFoundError:
    pass

print(f"Server is running on {server_address}")

socket.bind(server_address)
socket.listen(1)

while True:
    connection, client_address = socket.accept()
    try:
        print(f"Connection from {client_address}")
        while True:
            data = connection.recv(16)
            data_str = data.decode('utf-8')
            if data:
                print(f"Received message: {data_str}")
                response = 'Processing' + data_str
                connection.sendall(response.encode('utf-8'))
            else:
                print(f"No data received from {client_address}")
                break
    finally:
        print("Connection closed")
        connection.close()
