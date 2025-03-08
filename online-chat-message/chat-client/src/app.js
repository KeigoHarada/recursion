/**
 * チャットアプリケーション - メインエントリーポイント
 * SOLID原則に基づいたモジュール設計
 */

import ChatService from "./services/ChatService.js";
import UIController from "./controllers/UIController.js";

/**
 * アプリケーション初期化
 */
document.addEventListener("DOMContentLoaded", () => {
  console.log("DOM fully loaded");

  try {
    // 依存性注入の原則に従い、ChatServiceをUIControllerに注入
    const chatService = new ChatService();
    const uiController = new UIController(chatService);

    console.log("チャットアプリケーションが初期化されました");
  } catch (error) {
    console.error("アプリケーション初期化エラー:", error);
  }
});
