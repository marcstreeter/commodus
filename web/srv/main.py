import argparse
import asyncio
import os.path


from tornado.platform.asyncio import AsyncIOMainLoop
from tornado.web import Application
from tornado.web import StaticFileHandler
from tornado.httpserver import HTTPServer
from tornado.options import define

from libs import setup

from handlers import (
    IndividualView,
    TwilioView,
    WebSocketHandler
)
from handlers.websocket.view import infinite_update_loop


# CONSTANTS
parser = argparse.ArgumentParser(description='commodus')
parser.add_argument('dbuser', help='database username string')
parser.add_argument('dbpass', help='database password string')
parser.add_argument('dbhost', help='database host string (ex: 120.0.0.1)')
parser.add_argument('dbname', help='database name string')
parser.add_argument('--dbport', help='database port integer (ex: 5432)', type=int, default=5432)
parser.add_argument('--port', help='API server port integer (ex: 8080)', type=int, default=8080)
config = parser.parse_args()
define('username', default=config.dbuser, type=str, group='db')
define('password', default=config.dbpass, type=str, group='db')
define('host', default=config.dbhost, type=str, group='db')
define('name', default=config.dbname, type=str, group='db')
define('port', default=config.dbport, type=int, group='db')

logger = setup.log(name='commodus', version='v1')


def main():
    AsyncIOMainLoop().install()
    server = HTTPServer(
        Application(
            [
                (r'/v1/twilio/', TwilioView),
                (r"/v1/individual/([0-9A-F]{32})", IndividualView),
                (r'/static/(.*)', StaticFileHandler, {'path': 'static'}),
                (r'/ws', WebSocketHandler),
                (r'/(.*)', StaticFileHandler, {'path': 'static', 'default_filename': 'index.html'}),
            ],
            # default_handler_class=NotFoundView,
            template_path=os.path.join(os.path.dirname(__file__), "static")
        )
    )
    server.bind(8080)
    server.start()  # Forks multiple sub-processes
    logger.info("installing background services")
    asyncio.ensure_future(infinite_update_loop())
    logger.info("server is waiting for a connection")
    asyncio.get_event_loop().run_forever().start()

if __name__ == "__main__":
    main()
