"""
UDP通信を担当するクライアントモジュール
チャットメッセージの送受信を処理します
"""

import socket
import threading

class UDPClient:
    """UDPクライアント - メッセージ送受信を担当"""
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(1)  # 1秒タイムアウト（定期的にチェックするため）
        
    def send_message(self, room_id, token, message):
        """メッセージを送信"""
        try:
            # ヘッダーを構築
            room_id_bytes = room_id.encode('utf-8')
            room_id_size = len(room_id_bytes)
            token_bytes = token.encode('utf-8')
            token_size = len(token_bytes)
            message_bytes = message.encode('utf-8')
            
            # データパケットを構築
            header = bytearray(2)
            header[0] = room_id_size
            header[1] = token_size
            
            # メッセージを送信
            packet = header + room_id_bytes + token_bytes + message_bytes
            self.socket.sendto(packet, (self.host, self.port))
            
        except Exception as e:
            raise Exception(f"メッセージ送信エラー: {e}")
        
    def receive_message(self):
        """メッセージを受信"""
        try:
            data, _ = self.socket.recvfrom(4096)
            message = data.decode('utf-8')
            return message
        except socket.timeout:
            # タイムアウトは通常の動作（定期的なチェックのため）
            return None
        except Exception as e:
            raise Exception(f"メッセージ受信エラー: {e}")
            
    def close(self):
        """ソケットをクローズ"""
        self.socket.close() 