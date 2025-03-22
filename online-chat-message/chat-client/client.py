"""
チャットクライアントのメインモジュール
TCPとUDPの通信を統合し、ユーザーインターフェースを提供します
"""

import argparse
import threading
import sys
import os
from tcp_client import TCPClient
from udp_client import UDPClient

class ChatClient:
    """チャットクライアントのメインクラス"""
    
    def __init__(self, server_host, tcp_port, udp_port):
        self.server_host = server_host
        self.tcp_port = tcp_port
        self.udp_port = udp_port
        self.username = None
        self.room_id = None
        self.room_name = None
        self.token = None
        self.tcp_client = TCPClient(server_host, tcp_port)
        self.udp_client = None
        self.running = False
        
    def start(self):
        """クライアントを起動"""
        self.print_welcome()
        self.username = input("ユーザー名を入力してください: ")
        
        while True:
            self.print_menu()
            choice = input("選択してください (1-3): ")
            
            if choice == '1':
                self.create_room()
            elif choice == '2':
                self.join_room()
            elif choice == '3':
                print("チャットクライアントを終了します。")
                sys.exit(0)
            else:
                print("無効な選択です。もう一度選択してください。")
    
    def print_welcome(self):
        """ウェルカムメッセージを表示"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("====================================")
        print("     オンラインチャットクライアント     ")
        print("====================================")
        
    def print_menu(self):
        """メインメニューを表示"""
        print("\nメインメニュー:")
        print("1. 新しいチャットルームを作成")
        print("2. 既存のチャットルームに参加")
        print("3. 終了")
        
    def create_room(self):
        """新しいルームを作成"""
        room_name = input("作成するルーム名を入力してください: ")
        try:
            result = self.tcp_client.create_room(room_name, self.username)
            if result:
                self.token = result['token']
                self.room_id = result['roomId']
                self.room_name = room_name
                print(f"ルーム '{room_name}' を作成しました！")
                self.start_chat()
            else:
                print("ルームの作成に失敗しました。")
        except Exception as e:
            print(f"エラー: {e}")
            
    def join_room(self):
        """既存のルームに参加"""
        room_id = input("参加するルームIDを入力してください: ")
        try:
            result = self.tcp_client.join_room(room_id, self.username)
            if result:
                self.token = result['token']
                self.room_id = result['roomId']
                self.room_name = result['roomName']
                print(f"ルーム '{self.room_name}' に参加しました！")
                self.start_chat()
            else:
                print("ルームへの参加に失敗しました。")
        except Exception as e:
            print(f"エラー: {e}")
            
    def start_chat(self):
        """チャットセッションを開始"""
        self.running = True
        # UDPクライアントを初期化
        self.udp_client = UDPClient(self.server_host, self.udp_port)
        
        # メッセージ受信スレッドを開始
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"==== ルーム: {self.room_name} (ID: {self.room_id}) ====")
        print("チャットを開始します。終了するには '/exit' と入力してください。")
        
        # メッセージ送信ループ
        while self.running:
            try:
                message = input()
                if message.lower() == '/exit':
                    self.running = False
                    break
                    
                if message:
                    self.udp_client.send_message(self.room_id, self.token, message)
            except KeyboardInterrupt:
                self.running = False
                break
            except Exception as e:
                print(f"エラー: {e}")
                
        print("チャットを終了します...")
        return
        
    def receive_messages(self):
        """メッセージ受信処理"""
        while self.running:
            try:
                message = self.udp_client.receive_message()
                if message:
                    print(message)
            except Exception as e:
                if self.running:  # 終了時のエラーは無視
                    print(f"受信エラー: {e}")
                    
def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(description="チャットクライアント")
    parser.add_argument('--host', default='localhost', help='サーバーホスト')
    parser.add_argument('--tcp-port', type=int, default=9001, help='TCPポート')
    parser.add_argument('--udp-port', type=int, default=10000, help='UDPポート')
    
    args = parser.parse_args()
    
    client = ChatClient(args.host, args.tcp_port, args.udp_port)
    try:
        client.start()
    except KeyboardInterrupt:
        print("\nクライアントを終了します。")
        sys.exit(0)

if __name__ == "__main__":
    main() 