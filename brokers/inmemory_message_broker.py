import queue
from queue import Queue

from models.model import Email


### In house message broker
class InMemoryMessageBroker:

    def __init__(self):
        self.queue: Queue[Email] = queue.Queue()


    def publish(self, message: Email):
        self.queue.put(message)

    def consume(self, timeout=None) -> Email:
        return self.queue.get(timeout=timeout)