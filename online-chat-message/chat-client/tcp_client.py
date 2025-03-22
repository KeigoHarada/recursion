"""
TCP通信を担当するクライアントモジュール
ルームの作成と参加を処理します
"""

import socket
import json

class TCPClient:
    """TCPクライアント - ルーム作成・参加を担当"""
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        
    def create_room(self, room_name, username):
        """新しいルームを作成"""
        return self._send_tcp_request(1, 0, room_name, username)
    
    def join_room(self, room_id, username):
        """既存のルームに参加"""
        return self._send_tcp_request(2, 0, room_id, username)
        
    def _send_tcp_request(self, operation, state, room_id, payload):
        """TCPリクエストを送信"""
        try:
            # TCPソケットを作成
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(10) # 10秒タイムアウト
            client_socket.connect((self.host, self.port))
            
            # ヘッダーを構築
            room_id_bytes = room_id.encode('utf-8')
            room_id_size = len(room_id_bytes)
            payload_bytes = payload.encode('utf-8')
            payload_size = len(payload_bytes)
            
            header = bytearray(32)
            header[0] = room_id_size
            header[1] = operation
            header[2] = state
            
            # ペイロードサイズをバイトに変換
            payload_size_str = str(payload_size)
            for i in range(min(len(payload_size_str), 29)):
                header[3 + i] = ord(payload_size_str[i])
            
            # リクエストを送信
            client_socket.send(header + room_id_bytes + payload_bytes)
            
            # レスポンスの受信
            response_header = client_socket.recv(32)
            if not response_header:
                raise ConnectionError("サーバーからのレスポンスがありません")
                
            response_room_size = response_header[0]
            response_operation = response_header[1]
            response_state = response_header[2]
            
            # ペイロードサイズの解析
            payload_size_bytes = response_header[3:32]
            response_payload_size_str = ''
            for b in payload_size_bytes:
                if b == 0:  # ヌルバイトで終了
                    break
                if 48 <= b <= 57:  # ASCIIの0-9
                    response_payload_size_str += chr(b)
                    
            response_payload_size = int(response_payload_size_str) if response_payload_size_str else 0
            
            # データの受信
            max_data_size = response_room_size + response_payload_size
            data = bytearray()
            total_received = 0
            
            while total_received < max_data_size:
                chunk = client_socket.recv(min(4096, max_data_size - total_received))
                if not chunk:
                    break
                data.extend(chunk)
                total_received += len(chunk)
                
            room_name = data[:response_room_size].decode('utf-8')
            
            if response_state == 2:  # エラー状態
                error_message = data[response_room_size:].decode('utf-8')
                raise ValueError(f"サーバーエラー: {error_message}")
                
            # ペイロードが存在する場合のみ処理
            if total_received > response_room_size:
                payload_json = data[response_room_size:].decode('utf-8')
                result = json.loads(payload_json)
                return result
            else:
                return None
                
        except socket.timeout:
            raise TimeoutError("サーバーへの接続がタイムアウトしました")
        except json.JSONDecodeError:
            raise ValueError("サーバーからの無効なJSONレスポンス")
        finally:
            client_socket.close() 