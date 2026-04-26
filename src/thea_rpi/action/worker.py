import queue
import numpy as np
from thea_rpi.action.base import BaseActor


class ActionConsumer:
    def __init__(self, command_queue: queue.Queue[tuple], actor: BaseActor):
        self.command_queue = command_queue
        self.actor = actor
        self.running = False


    def start(self) -> None:
        self.actor.start()
        self.running = True


    def run(self) -> None:
        while self.running:
            try:
                command = self.command_queue.get()
                self.actor.act(command)
                self.command_queue.task_done()
            except queue.Empty:
                pass


    def stop(self) -> None:
        self.running = False


if __name__ == "__main__":
    pass
