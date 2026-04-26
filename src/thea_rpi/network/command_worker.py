import queue, struct, threading
from thea_rpi.network.client import TCPClient


class CommandProducer:
    def __init__(self, command_queue: queue.Queue[tuple], send_event: threading.Event, client: TCPClient):
        self.command_queue = command_queue
        self.send_event = send_event
        self.client = client
        self.running = False


    def start(self) -> None:
        self.running = True


    def run(self) -> None:
        while self.running:
            try:
                data = self.client.receive()
                if data:
                    try:
                        command = struct.unpack('>2f', data)
                        self.command_queue.put_nowait(command)
                    except queue.Full:
                        pass
                    self.send_event.set()
            except Exception:
                pass


    def stop(self) -> None:
        self.running = False


if __name__ == "__main__":
    pass
