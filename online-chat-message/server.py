import socket
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class ClientInfo:
    address: str
    last_message_time: datetime
    def update_message_time(self):
        self.last_message_time = datetime.now()

class UDPServer:
    # UDPサーバーの作成
    def __init__(self, host: str = '127.0.0.1', port: int = 10000):
        self.host = host
        self.port = port
        self.socket = None

    def create_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host, self.port))

class ChatServer:
    _MESSAGE_SIZE:int = 4096
    _USERNAME_LENGTH:int = 1
    _USERNAME_SIZE:int = 255
    _INACTIVE_CLIENT_TIMEOUT:timedelta = timedelta(minutes=3)
    _CLIENTS:dict[str, ClientInfo] = {}

    def start(self):
        print("Server is starting...")
        self.udp_server = UDPServer()
        self.udp_server.create_socket()

        while True:
            username, message, address = self._receive_message()
            print(f"{username}: {message}")
            self._update_client(username, address)
            self._relay_message(username, message)

    def _receive_message(self):
        data, address = self.udp_server.socket.recvfrom(self._MESSAGE_SIZE)
        # username を読み取る
        username = self._recieve_username(data)
        # メッセージを読み取る
        message_data = data[self._USERNAME_LENGTH + len(username):]
        message = self._recieve_message(message_data)
        return username, message, address

    def _recieve_username(self, data):
        username_length_data = data[:self._USERNAME_LENGTH]
        username_length = int.from_bytes(username_length_data, 'big')
        username_data = data[self._USERNAME_LENGTH:self._USERNAME_LENGTH + username_length]
        username = username_data.decode()
        return username
    
    def _recieve_message(self, message_data):
        message = message_data.decode()
        return message
    
    def _update_client(self, username, address):
        if username not in self._CLIENTS:
            self._CLIENTS[username] = ClientInfo(address, datetime.now())
        else:
            self._CLIENTS[username].update_message_time()
        self._remove_inactive_clients()

    def _remove_inactive_clients(self):
        current_time = datetime.now()
        inactive_usernames = [
            username
            for username, client_info in self._CLIENTS.items()
            if client_info.last_message_time < current_time - self._INACTIVE_CLIENT_TIMEOUT
        ]
        for username in inactive_usernames:
            del self._CLIENTS[username]

    def _relay_message(self, sender_username: str, message: str) -> None:
        for username, client_info in self._CLIENTS.items():
            # 送信者以外にメッセージを転送
            if username != sender_username:
                data = f"{sender_username}: {message}".encode()
                self.udp_server.socket.sendto(data, client_info.address)

if __name__ == "__main__":
    server = ChatServer()
    server.start()