
from brokers.inmemory_message_broker import InMemoryMessageBroker
from models.model import Resources
from providers.email_provider import EmailProvider
from workers.email_worker import EmailWorker

class ApplicationResources:
    def __init__(self):
        self.inmemory_message_broker = InMemoryMessageBroker()
        self.email_provider = EmailProvider()


    def create_resources(self) -> Resources:
        worker: EmailWorker = EmailWorker(provider=self.email_provider, broker=self.inmemory_message_broker)
        return Resources(worker=worker)