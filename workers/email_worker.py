import queue
from queue import Empty
from threading import Thread

from brokers.inmemory_message_broker import InMemoryMessageBroker
from providers.email_provider import EmailProvider


class EmailWorker:
    def __init__(self, provider: EmailProvider, broker: InMemoryMessageBroker) -> None:
        self.email_provider = provider
        self.broker = broker
        self.thread = Thread(target=self.run)

        ## execution control of the worker
        self.running = False


    def run(self) -> None:
        ## TODO: add graceful shutdown
        while self.running:
            try:
                email = self.broker.consume(timeout=1)
                self.email_provider.send_email(email)
            except Empty:
                continue
            except Exception as e:
                ## TODO: add structured logging
                print(e)

    def start(self):
        self.running = True
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()