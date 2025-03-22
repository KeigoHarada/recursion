"""
UDP通信を処理するサーバーモジュール
チャットメッセージのリアルタイム配信を担当します
"""

import socket
import threading
from datetime import datetime, timedelta

class UDPServer:
    """UDPサーバー - チャットメッセージを処理"""
    def __init__(self, tcp_server, host='0.0.0.0', port=10000):
        self.host = host
        self.port = port
        self.socket = None
        self.tcp_server = tcp_server
        self.running = False

    def start(self):
        """サーバーを起動"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host, self.port))
        self.running = True
        print(f"UDP Server running on {self.host}:{self.port}")

        while self.running:
            try:
                data, address = self.socket.recvfrom(4096)
                self.handle_message(data, address)
            except Exception as e:
                print(f"UDP message error: {e}")

    def handle_message(self, data, address):
        """UDPメッセージの処理"""
        try:
            # ヘッダー解析
            room_id_size = data[0]
            token_size = data[1]
            
            # データの解析
            room_id = data[2:2+room_id_size].decode('utf-8')
            token = data[2+room_id_size:2+room_id_size+token_size].decode('utf-8')
            message = data[2+room_id_size+token_size:].decode('utf-8')
            
            # ルームとトークンの検証
            if room_id not in self.tcp_server.rooms:
                print(f"Room {room_id} not found")
                return
                
            room = self.tcp_server.rooms[room_id]
            if token not in room.clients:
                print(f"Invalid token for room {room_id}")
                return
                
            # クライアント情報の更新
            client_info = room.clients[token]
            client_info.update_message_time()
            client_info.address = address  # アドレスの更新（IP変更に対応）
            
            # メッセージをルームの全クライアントに転送
            sender = client_info.username
            room.add_message(sender, message)
            
            formatted_message = f"{sender}: {message}".encode('utf-8')
            
            for client_address in room.get_client_addresses(token):
                self.socket.sendto(formatted_message, client_address)
                
        except Exception as e:
            print(f"Error handling UDP message: {e}")

    def remove_inactive_clients(self):
        """非アクティブなクライアントを削除"""
        current_time = datetime.now()
        timeout = timedelta(minutes=3)
        
        for room_id, room in list(self.tcp_server.rooms.items()):
            inactive_tokens = []
            
            for token, client in room.clients.items():
                if current_time - client.last_message_time > timeout:
                    inactive_tokens.append(token)
            
            room_active = True
            for token in inactive_tokens:
                # クライアント削除（ホストの場合はルームも削除）
                if not room.remove_client(token):
                    room_active = False
                    
            if not room_active or not room.clients:
                del self.tcp_server.rooms[room_id] 