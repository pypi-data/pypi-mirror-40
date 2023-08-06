import signal
from functools import wraps, partial
from collections import defaultdict

from curio import SignalEvent
from curio import run, spawn, tcp_server
from autoroutes import Routes

from trinket import lifecycle
from trinket.handler import request_handler
from trinket.request import Request
from trinket.http import HTTPStatus, HTTPError
from trinket.websockets import Websocket


Goodbye = SignalEvent(signal.SIGINT, signal.SIGTERM)


class Trinket:

    __slots__ = ('hooks', 'routes', 'websockets')

    def __init__(self):
        self.routes = Routes()
        self.websockets = set()
        self.hooks = defaultdict(list)

    async def lookup(self, request: Request):
        payload, params = self.routes.match(request.path)

        if not payload:
            raise HTTPError(HTTPStatus.NOT_FOUND, request.path)

        # Uppercased in order to only consider HTTP verbs.
        handler = payload.get(request.method.upper(), None)
        if handler is None:
            raise HTTPError(HTTPStatus.METHOD_NOT_ALLOWED)

        # We check if the route is for a websocket handler.
        # If it is, we make sure we were asked for an upgrade.
        if payload.get('websocket', False) and not request.upgrade:
            raise HTTPError(
                HTTPStatus.UPGRADE_REQUIRED,
                'This is a websocket endpoint, please upgrade.')

        return handler, params

    @lifecycle.handler_events
    async def __call__(self, request: Request):
        handler, params = await self.lookup(request)
        return await handler(request, **params)

    def route(self, path: str, methods: list=None, **extras: dict):
        if methods is None:
            methods = ['GET']

        def wrapper(func):
            payload = {method: func for method in methods}
            payload.update(extras)
            self.routes.add(path, **payload)
            return func

        return wrapper

    def websocket(self, path: str, **extras: dict):

        def wrapper(func):
            @wraps(func)
            async def websocket_handler(request, **params):
                websocket = Websocket(request.socket)
                try:
                    await websocket.upgrade(request)
                    self.websockets.add(websocket)
                    task = await spawn(func, request, websocket, **params)
                    await websocket.flow(task)
                finally:
                    self.websockets.discard(websocket)

            payload = {'GET': websocket_handler, 'websocket': True}
            payload.update(extras)
            self.routes.add(path, **payload)
            return func

        return wrapper

    def listen(self, name: str):
        def wrapper(func):
            self.hooks[name].append(func)
        return wrapper

    async def notify(self, name: str, *args, **kwargs):
        if name in self.hooks:
            for hook in self.hooks[name]:
                result = await hook(*args, **kwargs)
                if result is not None:
                    # Allows to shortcut the chain.
                    return result
        return None

    @lifecycle.server_events
    async def serve(self, host, port):
        print('Trinket serving on {}:{}'.format(host, port))
        handler = partial(request_handler, self)
        server = await spawn(tcp_server(host, port, handler))
        await Goodbye.wait()
        print('Server is shutting down.')
        print('Please wait. The remaining tasks are being terminated.')
        await server.cancel()

    def start(self, host='127.0.0.1', port=5000, debug=True):
        run(self.serve, host, port, with_monitor=debug)
        print('Trinket is crumbling away...')
