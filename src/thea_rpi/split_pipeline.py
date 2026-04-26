import queue, threading
from thea_rpi.action.base import BaseActor
from thea_rpi.network.client import TCPClient
from thea_rpi.network.frame_worker import FrameSender
from thea_rpi.network.command_worker import CommandProducer
from thea_rpi.action.worker import ActionConsumer


class SplitPipeline:
    def __init__(self, name: str, actor: BaseActor):
        self.name = name
        self.actor = actor


    def start(self) -> None:
        send_event = threading.Event()
        self.client = TCPClient()

        command_queue = queue.Queue(maxsize=30)
        self.command_producer = CommandProducer(command_queue, send_event, self.client)
        self.frame_sender = FrameSender(send_event, self.client)
        self.action_consumer = ActionConsumer(command_queue, self.actor)

        self.frame_sender_thread = threading.Thread(target=self.frame_sender.run, daemon=True)
        self.command_producer_thread = threading.Thread(target=self.command_producer.run, daemon=True)
        self.action_consumer_thread = threading.Thread(target=self.action_consumer.run, daemon=True)


    def run(self) -> None:
        self.command_producer.start()
        self.frame_sender.start()
        self.action_consumer.start()

        self.frame_sender_thread.start()
        self.command_producer_thread.start()
        self.action_consumer_thread.start()

        try:
            self.frame_sender_thread.join()
            self.command_producer_thread.join()
            self.action_consumer_thread.join()
        except KeyboardInterrupt:
            self.stop()


    def stop(self) -> None:
        self.frame_sender.stop()
        self.command_producer.stop()
        self.action_consumer.stop()
        self.client.close()


if __name__ == "__main__":
    pass
