from abc import ABC, abstractmethod
import socket, struct
from thea_rpi.config import SERVER_IP, PORT


class BaseClient(ABC):

    def __init__(self):
        self.socket = None


    @abstractmethod
    def start(self):
        pass


    @abstractmethod
    def send(self, data: bytes) -> None:
        pass


    def send_string(self, message: str) -> None:
        data = message.encode("utf-16")
        self.send(data)


    @abstractmethod
    def receive(self) -> bytes:
        pass


    def receive_string(self) -> str:
        data = self.receive()
        if not data:
            return ""
        
        return data.decode("utf-16")


    def close(self) -> None:
        if self.socket:
            self.socket.close()
            self.socket = None    


class TCPClient(BaseClient):

    def start(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((SERVER_IP, PORT))
        print(f"TCP Client connected to {SERVER_IP}:{PORT}")


    def send(self, data: bytes) -> None:
        if not self.socket:
            raise RuntimeError("Client not started. Call start() first")

        try:
            header = struct.pack(">I", len(data))
            self.socket.sendall(header + data)

        except Exception as e:
            print(f"TCP Client send error: {e}")
            self.close()


    def _recv_exactly(self, n: int) -> bytes:

        if not self.socket:
            raise RuntimeError("Client not started. Call start() first")

        data = b''
        while len(data) < n:
            packet = self.socket.recv(n - len(data))
            if not packet:
                return b''
            data += packet
        return data

    
    def receive(self) -> bytes:

        try:
            header = self._recv_exactly(4)
            if not header:
                self.close()
                return b''

            message_length = struct.unpack(">I", header)[0]
            message = self._recv_exactly(message_length)
            return message

        except Exception as e:
            print(f"TCP Client receive error: {e}")
            self.close()
            return b''
    
    
    def close(self) -> None:
        super().close()
        print("TCP Client closed")


class UDPClient(BaseClient):

    def start(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(f"UDP Client ready to send to {SERVER_IP}:{PORT}")


    def send(self, data: bytes) -> None:
        if not self.socket:
            raise RuntimeError("Client not started. Call start() first")

        self.socket.sendto(data, (SERVER_IP, PORT))

    
    def receive(self) -> bytes:
        if not self.socket:
            raise RuntimeError("Client not started. Call start() first")

        data, _ = self.socket.recvfrom(65535)
        return data
    

    def close(self) -> None:
        super().close()
        print("UDP Client closed")


if __name__ == "__main__":
    pass
