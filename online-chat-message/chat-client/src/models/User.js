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

export default User;
