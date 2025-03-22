"""
TCP接続を処理するサーバーモジュール
ルームの作成・参加などを管理します
"""

import socket
import threading
import json
import uuid
import traceback
from datetime import datetime
from models import ClientInfo, Room

class TCPServer:
    """TCPサーバー - ルーム作成・参加を処理"""
    def __init__(self, host='0.0.0.0', port=9001):
        self.host = host
        self.port = port
        self.socket = None
        self.rooms = {}  # roomId -> Room
        self.running = False

    def start(self):
        """サーバーを起動"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        self.running = True
        print(f"TCP Server running on {self.host}:{self.port}")

        while self.running:
            try:
                client_socket, address = self.socket.accept()
                client_handler = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, address)
                )
                client_handler.daemon = True
                client_handler.start()
            except Exception as e:
                print(f"TCP connection error: {e}")

    def handle_client(self, client_socket, address):
        """クライアント接続を処理"""
        try:
            # ヘッダーの受信 (32バイト)
            header = client_socket.recv(32)
            if not header:
                return

            room_name_size = header[0]
            operation = header[1]
            state = header[2]
            
            # ペイロードサイズの解析（安全に行う）
            payload_size_bytes = header[3:32]
            payload_size_str = ''
            for b in payload_size_bytes:
                if b == 0:  # ヌルバイトで終了
                    break
                if 48 <= b <= 57:  # ASCIIの0-9
                    payload_size_str += chr(b)
            
            try:
                payload_size = int(payload_size_str) if payload_size_str else 0
                print(f"受信ヘッダー: room_size={room_name_size}, op={operation}, state={state}, payload_size={payload_size}")
                
                # 最大サイズを制限
                MAX_PAYLOAD_SIZE = 10240  # 10KB
                if payload_size > MAX_PAYLOAD_SIZE:
                    print(f"警告: ペイロードサイズが大きすぎます ({payload_size} > {MAX_PAYLOAD_SIZE})。制限値に設定します。")
                    payload_size = MAX_PAYLOAD_SIZE
                    
            except ValueError:
                print(f"警告: ペイロードサイズの解析エラー。デフォルト値を使用します。")
                payload_size = 1024  # デフォルト値
            
            # データの受信
            max_data_size = room_name_size + payload_size
            print(f"データ受信サイズ: {max_data_size} バイト")
            
            data = bytearray()
            total_received = 0
            
            while total_received < max_data_size:
                chunk = client_socket.recv(min(4096, max_data_size - total_received))
                if not chunk:
                    break
                data.extend(chunk)
                total_received += len(chunk)
                
            if total_received < room_name_size:
                print("エラー: ルーム名を完全に受信できませんでした")
                return
                
            room_name = data[:room_name_size].decode('utf-8', errors='replace')
            
            # ペイロードが存在する場合のみ処理
            if total_received > room_name_size:
                payload = data[room_name_size:].decode('utf-8', errors='replace')
            else:
                payload = ""
                
            print(f"受信データ: room_name={room_name}, payload_length={len(payload)}")
            print(f"Debug - 受信ヘッダー: {', '.join([f'{b:02x}' for b in header[:8]])}")

            # 操作に応じた処理
            if operation == 1 and state == 0:  # ルーム作成リクエスト
                self.handle_create_room(client_socket, room_name, payload, address)
            elif operation == 2 and state == 0:  # ルーム参加リクエスト
                self.handle_join_room(client_socket, room_name, payload, address)

        except Exception as e:
            print(f"Error handling TCP client: {e}")
            traceback.print_exc()

    def handle_create_room(self, client_socket, room_name, username, address):
        """ルーム作成処理"""
        try:
            # 新しいルームの作成
            room = Room(room_name)
            self.rooms[room.id] = room
            
            # トークンの生成とホスト登録
            token = str(uuid.uuid4())
            client_info = ClientInfo(
                address=address,
                last_message_time=datetime.now(),
                username=username,
                is_host=True
            )
            
            room.add_client(token, client_info, is_host=True)
            
            # レスポンスの構築
            payload = json.dumps({
                "token": token,
                "roomId": room.id
            })
            
            # ペイロードサイズの確認（サイズが大きすぎる場合は切り詰める）
            if len(payload) > 1000:  # 安全なサイズ制限
                print(f"Warning: Payload too large ({len(payload)} bytes), truncating")
                payload = payload[:1000]
            
            # ステータスコードの送信
            response_header = bytearray(32)
            response_header[0] = len(room_name)
            response_header[1] = 1  # オペレーション（作成）
            response_header[2] = 1  # ステータス（応答）
            
            # バイト変換をより安全に行う
            payload_size_str = str(len(payload))
            for i in range(min(len(payload_size_str), 29)):
                response_header[3 + i] = ord(payload_size_str[i])
            # 残りは0で埋める
            for i in range(len(payload_size_str), 29):
                response_header[3 + i] = 0
            
            print(f"レスポンス送信: room_name={room_name}, payload_size={len(payload)}")
            print(f"Debug - レスポンスヘッダー: {', '.join([f'{b:02x}' for b in response_header[:8]])}")
            client_socket.send(response_header + room_name.encode('utf-8') + payload.encode('utf-8'))
            
            print(f"Room created: {room_name} (ID: {room.id})")
            
        except Exception as e:
            print(f"Error creating room: {e}")
            traceback.print_exc()
            
            # エラーレスポンスの構築
            error_header = bytearray(32)
            error_header[0] = len(room_name)
            error_header[1] = 1  # オペレーション（作成）
            error_header[2] = 2  # ステータス（エラー）
            error_message = str(e)[:100]  # 長すぎるエラーメッセージを防止
            
            # エラーメッセージサイズを安全に設定
            error_size_str = str(len(error_message))
            for i in range(min(len(error_size_str), 29)):
                error_header[3 + i] = ord(error_size_str[i])
            for i in range(len(error_size_str), 29):
                error_header[3 + i] = 0
                
            client_socket.send(error_header + room_name.encode('utf-8') + error_message.encode('utf-8'))

    def handle_join_room(self, client_socket, room_id, username, address):
        """ルーム参加処理"""
        try:
            if room_id not in self.rooms:
                raise ValueError("Room not found")
            
            room = self.rooms[room_id]
            
            # トークンを生成
            token = str(uuid.uuid4())
            client_info = ClientInfo(
                address=address,
                last_message_time=datetime.now(),
                username=username
            )
            
            room.add_client(token, client_info)
            
            # レスポンスの構築
            payload = json.dumps({
                "token": token,
                "roomId": room_id,
                "roomName": room.name
            })
            
            # ペイロードサイズの確認
            if len(payload) > 1000:
                print(f"Warning: Payload too large ({len(payload)} bytes), truncating")
                payload = payload[:1000]
            
            # ステータスコードの送信
            response_header = bytearray(32)
            response_header[0] = len(room_id)
            response_header[1] = 2  # オペレーション（参加）
            response_header[2] = 1  # ステータス（応答）
            
            # バイト変換を安全に行う
            payload_size_str = str(len(payload))
            for i in range(min(len(payload_size_str), 29)):
                response_header[3 + i] = ord(payload_size_str[i])
            # 残りは0で埋める
            for i in range(len(payload_size_str), 29):
                response_header[3 + i] = 0
            
            print(f"ルーム参加レスポンス送信: room_id={room_id}, payload_size={len(payload)}")
            print(f"Debug - レスポンスヘッダー: {', '.join([f'{b:02x}' for b in response_header[:8]])}")
            client_socket.send(response_header + room_id.encode('utf-8') + payload.encode('utf-8'))
            
            print(f"Client joined room: {room_id} - {username}")
            
        except Exception as e:
            print(f"Error joining room: {e}")
            traceback.print_exc()
            
            # エラーレスポンスの構築
            error_header = bytearray(32)
            error_header[0] = len(room_id)
            error_header[1] = 2  # オペレーション（参加）
            error_header[2] = 2  # ステータス（エラー）
            error_message = str(e)[:100]  # 長すぎるエラーメッセージを防止
            
            # エラーメッセージサイズを安全に設定
            error_size_str = str(len(error_message))
            for i in range(min(len(error_size_str), 29)):
                error_header[3 + i] = ord(error_size_str[i])
            # 残りは0で埋める
            for i in range(len(error_size_str), 29):
                error_header[3 + i] = 0
                
            client_socket.send(error_header + room_id.encode('utf-8') + error_message.encode('utf-8')) 