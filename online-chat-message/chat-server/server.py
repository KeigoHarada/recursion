"""
オンラインチャットメッセージサーバー
TCP接続でルーム作成・参加を管理し、UDPでリアルタイムメッセージを配信します
"""

import threading
from tcp_server import TCPServer
from udp_server import UDPServer

def start_servers():
    """サーバーを起動"""
    # TCPサーバーの作成
    tcp_server = TCPServer()
    tcp_thread = threading.Thread(target=tcp_server.start)
    tcp_thread.daemon = True
    tcp_thread.start()
    
    # UDPサーバーの作成
    udp_server = UDPServer(tcp_server)
    udp_thread = threading.Thread(target=udp_server.start)
    udp_thread.daemon = True
    udp_thread.start()
    
    # 非アクティブクライアント削除の定期実行
    def cleanup_task():
        while True:
            try:
                udp_server.remove_inactive_clients()
            except Exception as e:
                print(f"Cleanup error: {e}")
            threading.Event().wait(60)  # 1分ごとに実行
            
    cleanup_thread = threading.Thread(target=cleanup_task)
    cleanup_thread.daemon = True
    cleanup_thread.start()
    
    # メインスレッドを維持
    try:
        while True:
            threading.Event().wait(10)
    except KeyboardInterrupt:
        print("Shutting down servers...")

if __name__ == "__main__":
    start_servers()