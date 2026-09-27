from starlette.requests import Request



def get_broker(request: Request):
    return request.app.state.resources.broker