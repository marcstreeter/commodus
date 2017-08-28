import asyncio
import json
import os.path
import time
import uuid

from tornado.platform.asyncio import to_asyncio_future
from tornado.platform.asyncio import AsyncIOMainLoop
from tornado.web import Application
from tornado.web import RequestHandler
from tornado.web import StaticFileHandler
from tornado.httpserver import HTTPServer
from tornado.websocket import WebSocketHandler


from libs import setup


# CONSTANTS
UPDATE_PERIOD = 10


logger = setup.log(name='commodus', version='v1')


connections = []


class FaviconHandler(RequestHandler):
    def get(self):
        self.redirect('/static/favicon.ico')


class WebHandler(RequestHandler):
    def get(self):
        self.render("/static/index.html")


class WSHandler(WebSocketHandler):
    def open(self):
        logger.debug('new connection')
        connections.append(self)
        self.write_message(
            {
                "message": str(uuid.uuid4())
            }
        )

    def on_message(self, message):
        """
        expects a message of this format
        {
            'command': <name of command>,
            'kwargs': <inputs for the command>
        }
        :param message:
        :return:
        """
        logger.debug(f'message received: "{message}"')
        msg = json.loads(message)
        logger.debug(f'message parsed: "{msg}"')

    def on_close(self):
        logger.debug('connection closed')
        connections.remove(self)


async def update():

    while True:
        await asyncio.sleep(UPDATE_PERIOD)  # switch to other code and continue execution in 5 seconds

        msg = {
            'messages': [
                {'id': str(uuid.uuid4()), 'ts': int(time.time()), 'body': 'hello'},
                {'id': str(uuid.uuid4()), 'ts': int(time.time()), 'body': 'yes, what?'}
            ]
        }
        if update:
            logger.debug(f"sending update, next update in {UPDATE_PERIOD}")
            for connection in connections:
                await to_asyncio_future(
                    connection.write_message(msg)
                )# send message to each connected client
        else:
            logger.debug(f"next update in {UPDATE_PERIOD}")


def main():
    #asyncio.ensure_future(echo_forever())  # fire and forget
    AsyncIOMainLoop().install()
    server = HTTPServer(
        Application(
            [
                (r'/favicon.ico', FaviconHandler),
                (r'/static/(.*)', StaticFileHandler, {'path': 'static'}),
                (r'/ws', WSHandler),
                (r'/(.*)', StaticFileHandler, {'path': 'static', 'default_filename': 'index.html'}),
            ],
            # default_handler_class=NotFoundView,
            template_path=os.path.join(os.path.dirname(__file__), "static")
        )
    )
    server.bind(8080)
    server.start()  # Forks multiple sub-processes
    logger.info("installing background services")
    asyncio.ensure_future(update())
    logger.info("server is waiting for a connection")
    asyncio.get_event_loop().run_forever().start()

if __name__ == "__main__":
    main()
