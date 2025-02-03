import socket
import sys
socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server_address = '/tmp/chat_socket'
print(f"Connecting to {server_address}")
try:
    socket.connect(server_address)
except:
    print(f"Failed to connect to {server_address}")
    sys.exit(1)

try:
    message = b'Hello, Server!'
    socket.sendall(message)
    socket.settimeout(2)
    try:
        while True:
            response = socket.recv(16)
            if response:
                print(f"Received response: {response.decode('utf-8')}")
            else:
                print(f"No response received from {server_address}")
                break
    except(TimeoutError):
        print(f"No response received from {server_address}")
finally:
    print("Closing connection")
    socket.close()

