import socket
import os
import faker

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)

socket.bind(server_address)
socket.listen(1)

print(f"Server is running on {server_address}")

while True:
    connection, client_address = socket.accept()
    try:
        print(f"Connection from {client_address}")
        while True:
            data = connection.recv(1024)
            data_str = data.decode('utf-8')
            if data:
                print(f"Received message: {data_str}")
                response = faker.Faker().sentence()
                connection.sendall(response.encode('utf-8'))
            else:
                print(f"No data received from {client_address}")
                break
    finally:
        print("Connection closed")
        connection.close()
