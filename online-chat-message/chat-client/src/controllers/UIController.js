import User from "../models/User.js";
import Message from "../models/Message.js";

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

    // デバッグ用
    console.log("UIController initialized");
    console.log("roomScreen:", this.roomScreen);
    console.log("chatScreen:", this.chatScreen);
    console.log("createRoomBtn:", this.createRoomBtn);
    console.log("joinRoomBtn:", this.joinRoomBtn);
  }

  _initEventListeners() {
    // ルーム作成
    this.createRoomBtn.addEventListener("click", () => {
      console.log("Create room button clicked");
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
      console.log("Join room button clicked");
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
      console.log(`Creating room: ${roomName}, username: ${username}`);
      const room = this.chatService.createRoom(roomName);
      this.currentUser = new User(username);
      this.currentRoom = room;

      this._switchToChat();
      this._updateRoomInfo();
      console.log("Switched to chat screen after creating room");
    } catch (error) {
      console.error("Error creating room:", error);
      alert(`エラー: ${error.message}`);
    }
  }

  _joinRoom(roomId, username) {
    try {
      console.log(`Joining room: ${roomId}, username: ${username}`);
      const room = this.chatService.joinRoom(roomId);
      this.currentUser = new User(username);
      this.currentRoom = room;

      this._switchToChat();
      this._updateRoomInfo();
      this._loadMessages();
      console.log("Switched to chat screen after joining room");
    } catch (error) {
      console.error("Error joining room:", error);
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
        console.error("Error sending message:", error);
        alert(`メッセージ送信エラー: ${error.message}`);
      }
    }
  }

  _leaveRoom() {
    console.log("Leaving room");
    this.currentRoom = null;
    this._switchToRoomScreen();
  }

  _switchToChat() {
    console.log("Switching to chat screen");
    this.chatMessagesElement.innerHTML = "";
    this.messageInput.focus();
  }

  _switchToRoomScreen() {
    console.log("Switching to room screen");

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

export default UIController;
