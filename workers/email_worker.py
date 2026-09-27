from brokers.inmemory_message_broker import InMemoryMessageBroker
from providers.email_provider import EmailProvider


class EmailWorker:
    def __init__(self, provider: EmailProvider, broker: InMemoryMessageBroker) -> None:
        self.email_provider = provider
        self.broker = broker

    def run(self) -> None:
        ## TODO: add graceful shutdown
        while True:
            try:
                email = self.broker.consume()
                self.email_provider.send_email(email)
            except Exception as e:
                ## TODO: add structured logging
                print(e)
