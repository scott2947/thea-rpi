import queue
import threading
from thea_rpi.network.client import TCPClient
from thea_rpi.network.processing import print_command


class CommandProducer:
    def __init__(self, client: TCPClient, command_queue: queue.Queue[str]):
        self.client = client
        self.command_queue = command_queue
        self.running = True


    def run(self) -> None:
        while self.running:
            try:
                command = self.client.receive_string()
                if command:
                    try:
                        self.command_queue.put_nowait(command)
                    except queue.Full:
                        pass
            except Exception:
                pass


class CommandConsumer:
    def __init__(self, command_queue: queue.Queue[str], operation):
        self.command_queue = command_queue
        self.operation = operation
        self.running = True


    def run(self) -> None:
        while self.running:
            try:
                command = self.command_queue.get()
                self.operation(command)
                self.command_queue.task_done()
            except queue.Empty:
                pass


class CommandController:
    def __init__(self, operation):
        self.client = TCPClient()
        self.shared_queue = queue.Queue(maxsize=30)

        self.producer = CommandProducer(self.client, self.shared_queue)
        self.consumer = CommandConsumer(self.shared_queue, operation)

        self.producer_thread = threading.Thread(target=self.producer.run, daemon=True)
        self.consumer_thread = threading.Thread(target=self.consumer.run, daemon=True)


    def start(self) -> None:
        self.client.start()
        self.client.send_string("Client hello")

        self.producer_thread.start()
        self.consumer_thread.start()

        try:
            self.producer_thread.join()
            self.consumer_thread.join()
        except KeyboardInterrupt:
            self.producer_thread.running = False
            self.consumer_thread.running = False
            self.client.close()


if __name__ == "__main__":
    cc = CommandController(print_command)
    cc.start()
