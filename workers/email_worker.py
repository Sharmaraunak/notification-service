from brokers.inmemory_message_broker import InMemoryMessageBroker
from providers.email_provider import EmailProvider


class EmailWorker:

    email_provider: EmailProvider
    broker: InMemoryMessageBroker

    def __init__(self, provider: EmailProvider, broker: InMemoryMessageBroker) -> None:
        self.email_provider = provider
        self.broker = broker


    def run(self) -> None:
        while True:
            try:
                email = self.broker.consume()
                self.email_provider.send_email(email)
            except Exception as e:
                print(e)
