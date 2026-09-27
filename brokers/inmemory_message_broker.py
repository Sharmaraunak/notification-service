
from uuid import UUID
from queue import Queue
from typing import Dict

from models.model import Email


### In house message broker
class InMemoryMessageBroker:

    def __init__(self):
        self.queue: Queue[Email] = Queue()
        self.dead_letter_queue: Queue[Email] = Queue()
        self.processing_map: Dict[UUID, Email] = {}
        self.MAX_RETRIES = 3


    def publish(self, message: Email):
        self.queue.put(item=message)

    def consume(self, timeout=None) -> Email:
        email: Email = self.queue.get(timeout=timeout)
        self.processing_map[email.id] = email
        return email

    def move_to_dead_letter_queue(self, message: Email):
        self.acknowledge(message_id=message.id)
        self.dead_letter_queue.put(item=message)

    def acknowledge(self, message_id: UUID):
        del self.processing_map[message_id]