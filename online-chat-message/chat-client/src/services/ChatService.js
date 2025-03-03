import Room from "../models/Room.js";
import Message from "../models/Message.js";

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

export default ChatService;
