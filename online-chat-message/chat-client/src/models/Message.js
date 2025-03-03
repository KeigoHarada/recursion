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

export default Message;
