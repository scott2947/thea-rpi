import queue, json
from thea_rpi.network.client import TCPClient


class CommandProducer:
    def __init__(self, command_queue: queue.Queue[dict]):
        self.command_queue = command_queue
        self.client = TCPClient()
        self.running = False


    def start(self) -> None:
        self.client.start()
        self.client.send_string("Client hello")

        self.running = True


    def run(self) -> None:
        while self.running:
            try:
                data = self.client.receive_string()
                if data:
                    try:
                        command = json.loads(data)
                        self.command_queue.put_nowait(command)
                    except queue.Full:
                        pass
            except Exception:
                pass


    def stop(self) -> None:
        self.running = False
        self.client.close()


if __name__ == "__main__":
    pass
