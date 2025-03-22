"""
チャットシステムのデータモデルを定義するモジュール
"""

import uuid
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ClientInfo:
    """クライアント情報を格納するデータクラス"""
    address: tuple
    last_message_time: datetime
    username: str
    is_host: bool = False
    
    def update_message_time(self):
        """最終メッセージ時間を更新"""
        self.last_message_time = datetime.now()


class Room:
    """チャットルームクラス"""
    def __init__(self, name, password=None):
        self.id = str(uuid.uuid4())[:8]  # 短いIDを生成
        self.name = name
        self.password = password
        self.clients = {}  # token -> ClientInfo
        self.host_token = None
        self.messages = []

    def add_client(self, token, client_info, is_host=False):
        """クライアントをルームに追加"""
        self.clients[token] = client_info
        if is_host:
            self.host_token = token
            client_info.is_host = True

    def remove_client(self, token):
        """クライアントをルームから削除
        
        戻り値:
            bool: ルームが有効かどうか（ホストが退出したらFalse）
        """
        if token in self.clients:
            del self.clients[token]
        # ホストが退出したら部屋を閉じる
        if token == self.host_token:
            return False
        return True

    def get_client_addresses(self, except_token=None):
        """特定のクライアントを除くすべてのクライアントのアドレスリストを取得"""
        return [client.address for token, client in self.clients.items() if token != except_token]

    def add_message(self, sender, content):
        """メッセージをルームに追加"""
        message = {
            "sender": sender,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.messages.append(message)
        return message 