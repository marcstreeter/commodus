import asyncio
import json
import logging
import uuid

import queries
from tornado.options import options
from tornado.platform.asyncio import to_asyncio_future

UPDATE_PERIOD = 10

from tornado.websocket import WebSocketHandler

logger = logging.getLogger(__name__)

connections = []

async def infinite_update_loop():
    while True:
        await asyncio.sleep(UPDATE_PERIOD)  # switch to other code and continue execution in 5 seconds

        db = options.group_dict('db')
        dbpass = db['password']
        dbuser = db['username']
        dbhost = db['host']
        dbname = db['name']
        dbport = db['port']

        session = queries.TornadoSession(
            f'postgresql://{dbuser}:{dbpass}@{dbhost}:{dbport}/{dbname}'
        )

        ## DETERMINE IF THERE WAS AN UPDATE OR NOT BY CHECKING IN THE PASSED XX SECONDS (which should coincide with
        ## HOW EVER LONG WE WAIT BAHHHH!HHH!HH!H!!HHHH
        if update:
            logger.debug(f"sending update, next update in {UPDATE_PERIOD}")
            for connection in connections:
                await to_asyncio_future(
                    connection.write_message(msg)
                )# send message to each connected client
        else:
            logger.debug(f"next update in {UPDATE_PERIOD}")


class Handler(WebSocketHandler):
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