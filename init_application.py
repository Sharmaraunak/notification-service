
from threading import Thread

from application_resources import ApplicationResources


def init_app():

    ## create the resources
    application_resources = ApplicationResources()
    resources = application_resources.create_resources()

    ## start the worker
    thread = Thread(target=resources.worker.run);
    thread.start()

    ## running the application
    yield

    ## TODO: graceful shutdown
