from abc import ABC, abstractmethod
import socket, struct
from thea_rpi.config import SERVER_IP, PORT


class BaseClient(ABC):

    def __init__(self):
        self.socket = None


    @abstractmethod
    def connect(self):
        pass


    @abstractmethod
    def send(self, data: bytes) -> None:
        pass


    def send_string(self, message: str) -> None:
        data = message.encode("utf-16")
        self.send(data)


    def close(self) -> None:
        if self.socket:
            self.socket.close()
            self.socket = None    


class TCPClient(BaseClient):

    def connect(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((SERVER_IP, PORT))
        print(f"TCP Client connected to {SERVER_IP}:{PORT}")


    def send(self, data: bytes) -> None:
        if not self.socket:
            raise RuntimeError("Client not connected. Call connect() first")

        try:
            header = struct.pack(">I", len(data))
            self.socket.sendall(header + data)

        except Exception as e:
            print(f"TCP Client send error: {e}")


    def close(self) -> None:
        super().close()
        print("TCP Client closed")


class UDPClient(BaseClient):

    def connect(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(f"UDP Client ready to send to {SERVER_IP}:{PORT}")


    def send(self, data: bytes) -> None:
        if not self.socket:
            raise RuntimeError("Client not initialised")


        self.socket.sendto(data, (SERVER_IP, PORT))


    def close(self) -> None:
        super().close()
        print("UDP Client closed")


if __name__ == "__main__":
    pass
