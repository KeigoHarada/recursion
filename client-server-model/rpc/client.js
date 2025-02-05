const net = require("net");

class RPCClient {
  constructor(host = "localhost", port = 10000) {
    this.host = host;
    this.port = port;
    this.client = new net.Socket();
    this.requestId = 0;
    this.pendingRequests = new Map();
  }

  connect() {
    return new Promise((resolve, reject) => {
      this.client.connect(this.port, this.host, () => {
        console.log(`Connected to RPC server at ${this.host}:${this.port}`);
        this._setupMessageHandler();
        resolve();
      });

      this.client.on("error", (error) => {
        reject(new Error(`Connection failed: ${error.message}`));
      });
    });
  }

  _setupMessageHandler() {
    let buffer = "";
    this.client.on("data", (data) => {
      buffer += data.toString();

      try {
        const response = JSON.parse(buffer);
        const resolver = this.pendingRequests.get(response.id);
        if (resolver) {
          if (response.error) {
            resolver.reject(new Error(response.error.message));
          } else {
            resolver.resolve(response.result);
          }
          this.pendingRequests.delete(response.id);
        }
        buffer = "";
      } catch (e) {
        // JSONのパースに失敗した場合は、データが完全に届いていない可能性があるため待機
      }
    });
  }

  async call(method, params) {
    const requestId = ++this.requestId;
    const request = {
      method,
      params,
      id: requestId,
    };

    return new Promise((resolve, reject) => {
      this.pendingRequests.set(requestId, { resolve, reject });
      this.client.write(JSON.stringify(request) + "\n");
    });
  }

  close() {
    this.client.end();
  }
}

// 使用例
async function example() {
  const client = new RPCClient();

  try {
    await client.connect();

    // 数値計算の例
    const subtractResult = await client.call("subtract", [42, 23]);
    console.log("Subtract result:", subtractResult);

    const floorResult = await client.call("floor", [3.14]);
    console.log("Floor result:", floorResult);

    const nrootResult = await client.call("nroot", [16, 2]);
    console.log("Square root result:", nrootResult);

    // 文字列操作の例
    const reverseResult = await client.call("reverse", ["hello"]);
    console.log("Reverse result:", reverseResult);

    const anagramResult = await client.call("validAnagram", [
      "listen",
      "silent",
    ]);
    console.log("Valid anagram result:", anagramResult);

    // 配列操作の例
    const sortResult = await client.call("sort", [[3, 1, 4, 1, 5, 9]]);
    console.log("Sort result:", sortResult);
  } catch (error) {
    console.error("Error:", error.message);
  } finally {
    client.close();
  }
}

// クライアントの実行
if (require.main === module) {
  example().catch(console.error);
}

module.exports = RPCClient;
