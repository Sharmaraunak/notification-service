
from queue import Empty
from threading import Thread

from brokers.inmemory_message_broker import InMemoryMessageBroker
from models.model import Email
from providers.email_provider import EmailProvider


class EmailWorker:

    MAX_RETRIES = 3

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
                email: Email = self.broker.consume(timeout=1)

                while email.attempts < self.MAX_RETRIES:
                    try:
                        email.attempts += 1
                        self.email_provider.send_email(email)
                        break
                    except Exception:
                        continue
            except Empty:
                ## TODO: will be replaced with retry policy of the failed tasks
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