import socket
import threading
import queue
from typing import Optional

class ChatClient:
  _MESSAGE_SIZE:int = 4096
  _MESSAGE_TIMEOUT:int = 1
  def __init__(self, server_address: str, server_port: int):
    self.server_address = server_address
    self.server_port = server_port
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.sock.settimeout(self._MESSAGE_TIMEOUT)
    self.message_queue = queue.Queue()  # 受信メッセージのキュー
    self.is_sending_mode = False

  def send_message(self, username: str, message: str):
    username_length = len(username)
    send_data = username_length.to_bytes(1, 'big') + username.encode() + message.encode()
    # サーバへのデータ送信
    sent = self.sock.sendto(send_data, (self.server_address, self.server_port))

  def receive_message(self):
    try:
      recv_data, address = self.sock.recvfrom(self._MESSAGE_SIZE)
      return recv_data.decode()
    except socket.timeout:
      return None
    
  def close(self):
    self.sock.close()

  def start_receiving(self):
    receiver_thread = threading.Thread(target=self._receive_loop, daemon=True)
    receiver_thread.start()

  def _receive_loop(self):
    while True:
      message = self.receive_message()
      if message:
          self.message_queue.put(message)

  def enter_sending_mode(self):
    self.is_sending_mode = True

  def exit_sending_mode(self):
    self.is_sending_mode = False

  def get_next_message(self) -> Optional[str]:
    try:
      return self.message_queue.get_nowait()
    except queue.Empty:
      return None


if __name__ == "__main__":
  client = ChatClient('127.0.0.1', 10000)
  client.start_receiving()  # 受信スレッドを開始

  try:
    while True:
      # 通常モード：メッセージを表示
      while not client.is_sending_mode:
        message = client.get_next_message()
        if message:
          print(message)
        
        # 送信モードに変更
        import sys
        import select
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
          key = sys.stdin.read(1)  # 1文字読み込み
          if key.lower() == 'i':
            print("送信モードに入ります。メッセージを入力してください。")
            client.enter_sending_mode()
            break

      # 送信モード
      if client.is_sending_mode:
        username = input("username: ")
        message = input("message: ")
        client.send_message(username, message)
        client.exit_sending_mode()

  finally:
    client.close()
