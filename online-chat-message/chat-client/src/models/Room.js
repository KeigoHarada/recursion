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

export default Room;
