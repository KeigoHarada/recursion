/**
 * チャットアプリケーション
 * SOLID原則に基づいたモジュール設計
 */

// 単一責任の原則 (SRP): 各クラスは単一の責任を持つ
// 開放/閉鎖原則 (OCP): 拡張に対して開かれ、修正に対して閉じている
// リスコフの置換原則 (LSP): 派生クラスは基底クラスと置換可能
// インターフェース分離の原則 (ISP): クライアントは使用しないインターフェースに依存すべきでない
// 依存性逆転の原則 (DIP): 上位モジュールは下位モジュールに依存すべきでない

/**
 * ユーザーモデル - ユーザー情報を管理
 */
class User {
  constructor(username) {
    this.username = username;
  }

  getUsername() {
    return this.username;
  }
}

/**
 * メッセージモデル - メッセージデータを管理
 */
class Message {
  constructor(sender, content, timestamp) {
    this.sender = sender;
    this.content = content;
    this.timestamp = timestamp || new Date();
  }

  getFormattedTime() {
    return this.timestamp.toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });
  }
}

/**
 * ルームモデル - チャットルームを管理
 */
class Room {
  constructor(name, id) {
    this.name = name;
    this.id = id || this._generateRoomId();
    this.messages = [];
  }

  _generateRoomId() {
    return Math.random().toString(36).substring(2, 8).toUpperCase();
  }

  getName() {
    return this.name;
  }

  getId() {
    return this.id;
  }

  addMessage(message) {
    this.messages.push(message);
    return message;
  }

  getMessages() {
    return this.messages;
  }
}

/**
 * チャットサービス - バックエンドとの通信を管理
 * 実際のアプリではWebSocketやREST APIを使用
 */
class ChatService {
  constructor() {
    // ローカルストレージをモックデータベースとして使用
    this.rooms = {};
    this._loadFromStorage();
  }

  _loadFromStorage() {
    const savedRooms = localStorage.getItem("chat_rooms");
    if (savedRooms) {
      this.rooms = JSON.parse(savedRooms);
    }
  }

  _saveToStorage() {
    localStorage.setItem("chat_rooms", JSON.stringify(this.rooms));
  }

  createRoom(name) {
    const room = new Room(name);
    this.rooms[room.getId()] = {
      name: room.getName(),
      id: room.getId(),
      messages: [],
    };
    this._saveToStorage();
    return room;
  }

  joinRoom(roomId) {
    const roomData = this.rooms[roomId];
    if (!roomData) {
      throw new Error("ルームが見つかりません");
    }

    const room = new Room(roomData.name, roomData.id);
    // メッセージを復元
    if (roomData.messages) {
      roomData.messages.forEach((msg) => {
        room.addMessage(
          new Message(msg.sender, msg.content, new Date(msg.timestamp))
        );
      });
    }

    return room;
  }

  sendMessage(roomId, message) {
    if (!this.rooms[roomId]) {
      throw new Error("ルームが見つかりません");
    }

    // メッセージをルームに追加
    this.rooms[roomId].messages.push({
      sender: message.sender,
      content: message.content,
      timestamp: message.timestamp,
    });

    this._saveToStorage();
    return message;
  }

  getRoomList() {
    return Object.keys(this.rooms).map((id) => ({
      id,
      name: this.rooms[id].name,
    }));
  }
}

/**
 * UIコントローラー - ユーザーインターフェースを管理
 */
class UIController {
  constructor(chatService) {
    this.chatService = chatService;
    this.currentUser = null;
    this.currentRoom = null;

    // 画面要素
    this.roomScreen = document.getElementById("room-screen");
    this.chatScreen = document.getElementById("chat-screen");

    // ルーム作成・参加フォーム
    this.createRoomInput = document.getElementById("create-room-input");
    this.createUsernameInput = document.getElementById("create-username-input");
    this.createRoomBtn = document.getElementById("create-room-btn");

    this.joinRoomInput = document.getElementById("join-room-input");
    this.joinUsernameInput = document.getElementById("join-username-input");
    this.joinRoomBtn = document.getElementById("join-room-btn");

    // チャット画面要素
    this.roomNameElement = document.getElementById("room-name");
    this.roomIdElement = document.getElementById("room-id");
    this.usernameElement = document.getElementById("username");
    this.chatMessagesElement = document.getElementById("chat-messages");
    this.messageInput = document.getElementById("message-input");
    this.sendMessageBtn = document.getElementById("send-message-btn");
    this.leaveRoomBtn = document.getElementById("leave-room-btn");

    this._initEventListeners();
  }

  _initEventListeners() {
    // ルーム作成
    this.createRoomBtn.addEventListener("click", () => {
      const roomName = this.createRoomInput.value.trim();
      const username = this.createUsernameInput.value.trim();

      if (roomName && username) {
        this._createAndJoinRoom(roomName, username);
      } else {
        alert("ルーム名とユーザー名を入力してください");
      }
    });

    // ルーム参加
    this.joinRoomBtn.addEventListener("click", () => {
      const roomId = this.joinRoomInput.value.trim();
      const username = this.joinUsernameInput.value.trim();

      if (roomId && username) {
        this._joinRoom(roomId, username);
      } else {
        alert("ルームIDとユーザー名を入力してください");
      }
    });

    // メッセージ送信
    this.sendMessageBtn.addEventListener("click", () => {
      this._sendMessage();
    });

    // Enterキーでメッセージ送信
    this.messageInput.addEventListener("keypress", (e) => {
      if (e.key === "Enter") {
        this._sendMessage();
      }
    });

    // ルーム退出
    this.leaveRoomBtn.addEventListener("click", () => {
      this._leaveRoom();
    });
  }

  _createAndJoinRoom(roomName, username) {
    try {
      const room = this.chatService.createRoom(roomName);
      this.currentUser = new User(username);
      this.currentRoom = room;

      this._switchToChat();
      this._updateRoomInfo();
    } catch (error) {
      alert(`エラー: ${error.message}`);
    }
  }

  _joinRoom(roomId, username) {
    try {
      const room = this.chatService.joinRoom(roomId);
      this.currentUser = new User(username);
      this.currentRoom = room;

      this._switchToChat();
      this._updateRoomInfo();
      this._loadMessages();
    } catch (error) {
      alert(`エラー: ${error.message}`);
    }
  }

  _sendMessage() {
    const content = this.messageInput.value.trim();

    if (content && this.currentRoom && this.currentUser) {
      const message = new Message(this.currentUser.getUsername(), content);

      try {
        this.chatService.sendMessage(this.currentRoom.getId(), {
          sender: message.sender,
          content: message.content,
          timestamp: message.timestamp,
        });

        this._addMessageToUI(message, true);
        this.messageInput.value = "";
      } catch (error) {
        alert(`メッセージ送信エラー: ${error.message}`);
      }
    }
  }

  _leaveRoom() {
    this.currentRoom = null;
    this._switchToRoomScreen();
  }

  _switchToChat() {
    this.roomScreen.classList.remove("active");
    this.chatScreen.classList.add("active");
    this.chatMessagesElement.innerHTML = "";
    this.messageInput.focus();
  }

  _switchToRoomScreen() {
    this.chatScreen.classList.remove("active");
    this.roomScreen.classList.add("active");

    // フォームをリセット
    this.createRoomInput.value = "";
    this.createUsernameInput.value = "";
    this.joinRoomInput.value = "";
    this.joinUsernameInput.value = "";
  }

  _updateRoomInfo() {
    if (this.currentRoom) {
      this.roomNameElement.textContent = `ルーム: ${this.currentRoom.getName()}`;
      this.roomIdElement.textContent = `ルームID: ${this.currentRoom.getId()}`;
      this.usernameElement.textContent = `ユーザー名: ${this.currentUser.getUsername()}`;
    }
  }

  _loadMessages() {
    if (this.currentRoom) {
      const room = this.chatService.joinRoom(this.currentRoom.getId());
      this.chatMessagesElement.innerHTML = "";

      room.getMessages().forEach((msg) => {
        const isSent = msg.sender === this.currentUser.getUsername();
        this._addMessageToUI(msg, isSent);
      });

      // 最新メッセージにスクロール
      this.chatMessagesElement.scrollTop =
        this.chatMessagesElement.scrollHeight;
    }
  }

  _addMessageToUI(message, isSent) {
    const messageElement = document.createElement("div");
    messageElement.classList.add("message");
    messageElement.classList.add(isSent ? "sent" : "received");

    const messageInfo = document.createElement("div");
    messageInfo.classList.add("message-info");
    messageInfo.textContent = `${
      message.sender
    } • ${message.getFormattedTime()}`;

    const messageContent = document.createElement("div");
    messageContent.classList.add("message-content");
    messageContent.textContent = message.content;

    messageElement.appendChild(messageInfo);
    messageElement.appendChild(messageContent);

    this.chatMessagesElement.appendChild(messageElement);

    // 最新メッセージにスクロール
    this.chatMessagesElement.scrollTop = this.chatMessagesElement.scrollHeight;
  }
}

/**
 * アプリケーション初期化
 */
document.addEventListener("DOMContentLoaded", () => {
  const chatService = new ChatService();
  const uiController = new UIController(chatService);
});
