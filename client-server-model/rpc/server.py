import socket
import json
import math
from typing import Any, Dict, List, Tuple

class RPCMethod:
    def __init__(self, name: str, handler: callable, param_types: List[type]):
        self.name = name
        self.handler = handler
        self.param_types = param_types

class RPCHandler:
    def __init__(self):
        self._methods: Dict[str, RPCMethod] = {}
        self._register_default_methods()

    def _register_default_methods(self):
        self.register_method("floor", self._floor, [float])
        self.register_method("nroot", self._nroot, [float, float])
        self.register_method("reverse", self._reverse, [str])
        self.register_method("validAnagram", self._valid_anagram, [str, str])
        self.register_method("sort", self._sort, [list])
        self.register_method("subtract", self._subtract, [int, int])

    def register_method(self, name: str, handler: callable, param_types: List[type]):
        self._methods[name] = RPCMethod(name, handler, param_types)

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        try:
            method_name = request.get("method")
            params = request.get("params", [])
            request_id = request.get("id")

            if method_name not in self._methods:
                return self._create_error_response(request_id, "Method not found")

            method = self._methods[method_name]
            if not self._validate_params(params, method.param_types):
                return self._create_error_response(request_id, "Invalid parameters")

            result = method.handler(*params)
            return {
                "result": result,
                "id": request_id
            }
        except Exception as e:
            return self._create_error_response(request_id, str(e))

    def _validate_params(self, params: List[Any], param_types: List[type]) -> bool:
        return True
        # if len(params) != len(param_types):
        #     return False
        # return all(isinstance(param, param_type) for param, param_type in zip(params, param_types))

    def _create_error_response(self, request_id: int, message: str) -> Dict[str, Any]:
        return {
            "error": {"message": message},
            "id": request_id
        }

    # RPC メソッドの実装
    def _floor(self, x: float) -> int:
        return math.floor(x)

    def _nroot(self, x: float, n: float) -> float:
        return math.pow(x, 1/n)

    def _reverse(self, s: str) -> str:
        return s[::-1]

    def _valid_anagram(self, s: str, t: str) -> bool:
        return sorted(s) == sorted(t)

    def _sort(self, arr: list) -> list:
        return sorted(arr)

    def _subtract(self, a: int, b: int) -> int:
        return a - b

class SocketServer:
    def __init__(self, host: str = 'localhost', port: int = 10000):
        self.host = host
        self.port = port
        self.socket = None

    def create_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)

    def accept_connection(self) -> Tuple[socket.socket, Tuple[str, int]]:
        return self.socket.accept()

class RPCServer:
    def __init__(self, host: str = 'localhost', port: int = 10000):
        self.socket_server = SocketServer(host, port)
        self.rpc_handler = RPCHandler()

    def start(self):
        self.socket_server.create_socket()
        print(f"RPC Server listening on {self.socket_server.host}:{self.socket_server.port}")
        
        while True:
            connection, client_address = self.socket_server.accept_connection()
            try:
                while True:
                    data = connection.recv(4096)
                    if not data:
                        break

                    request = json.loads(data.decode())
                    response = self.rpc_handler.handle_request(request)
                    connection.sendall(json.dumps(response).encode())
            except Exception as e:
                print(f"Error handling client {client_address}: {e}")
            finally:
                connection.close()

if __name__ == "__main__":
    server = RPCServer()
    server.start()
    