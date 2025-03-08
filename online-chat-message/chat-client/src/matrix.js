/**
 * マトリックス風の背景を生成するスクリプト
 */
document.addEventListener("DOMContentLoaded", function () {
  const matrixRain = document.getElementById("matrix-rain");
  const characters =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789$+-*/=%\"'#&_(),.;:?!\\|{}<>[]^~";
  const japaneseChars = "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜｦﾝ";

  /**
   * マトリックス風の文字列を生成する関数
   */
  function generateMatrixRain() {
    // 既存の要素をクリア
    matrixRain.innerHTML = "";

    const rows = Math.floor(window.innerHeight / 15);

    // マトリックス風の文字列を生成
    for (let i = 0; i < rows; i++) {
      const column = document.createElement("span");
      column.style.top = i * 15 + "px";

      // ランダムな文字列を生成
      let content = "";
      const length = 15 + Math.random() * 20;
      const useJapanese = Math.random() > 0.5;
      const charSet = useJapanese ? japaneseChars : characters;

      for (let j = 0; j < length; j++) {
        content +=
          charSet.charAt(Math.floor(Math.random() * charSet.length)) + "\n";
      }

      column.textContent = content;
      column.style.animationDuration = 5 + Math.random() * 15 + "s";
      column.style.animationDelay = Math.random() * 8 + "s";
      column.style.opacity = 0.5 + Math.random() * 0.5;

      matrixRain.appendChild(column);
    }
  }

  // 初期生成
  generateMatrixRain();

  // 画面サイズが変わったときに再生成
  window.addEventListener("resize", generateMatrixRain);
});
