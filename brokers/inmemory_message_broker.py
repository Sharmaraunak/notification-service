import queue

from models.model import Email


### In house message broker
class InMemoryMessageBroker:

    def __init__(self):
        self.queue = queue.Queue()


    def publish(self, message):
        self.queue.put(message)

    def consume(self, timeout=None):
        return self.queue.get(timeout=timeout)