

from contextlib import asynccontextmanager

from fastapi import FastAPI

from application_resources import ApplicationResources

@asynccontextmanager
async def lifespan(app: FastAPI):

    ## create the resources
    application_resources = ApplicationResources()
    resources = application_resources.create_resources()

    ## save the resources in the app state
    app.state.resources = resources

    ## start the worker
    resources.worker.start()

    ## running the application
    yield

    resources.worker.stop()

    ## TODO: graceful shutdown
