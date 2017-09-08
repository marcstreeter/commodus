from collections import OrderedDict
import logging
import traceback

from tornado.gen import convert_yielded
from tornado.options import options
from tornado.web import HTTPError
import queries
from tornado.web import RequestHandler

from libs import errors


logger = logging.getLogger(__name__)


class BaseView(RequestHandler):
    def initialize(self):
        logger.debug("setting up db session")
        db = options.group_dict('db')
        dbpass = db['password']
        dbuser = db['username']
        dbhost = db['host']
        dbname = db['name']
        dbport = db['port']

        self.session = queries.TornadoSession(
            f'postgresql://{dbuser}:{dbpass}@{dbhost}:{dbport}/{dbname}'
        )

    async def prepare(self):
        logger.debug(f"requested  {self.request.path}")

        try:
            await convert_yielded(self.session.validate())
        except queries.OperationalError as e:
            raise HTTPError(503, f'failed to validate db session({e})')

        else:
            logger.debug("refreshed db session")

    def write_error(self, status_code, **kwargs):
        """
        handles output for all errors

        :param int status_code:
        :param dict kwargs:
        :return:
        """
        http_code = status_code

        if 400 <= http_code <= 499:
            try:
                exc_value = kwargs['exc_info'][1]
                logger.debug(exc_value.log_message)
                message = exc_value.reason
            except Exception as e:
                logger.debug(f"failed to extract error details({e})")
                message = "Invalid Request"
        else:
            exc_value = kwargs['exc_info'][1]

            if isinstance(exc_value, errors.CommodusErrors):
                message = exc_value.reason
                logger.debug(exc_value.message)
                http_code = exc_value.code
            else:
                try:
                    error_trace = "".join(
                        l for l in traceback.format_exception(*kwargs['exc_info'])
                    )
                    logger.error(f"failed request: {error_trace}")
                except Exception as e:
                    logger.debug(f"failed to list error trace({e})")

                message = "critical error"

        self.set_status(http_code)
        self.write({'message': message})

    @staticmethod
    def prepare_output(output, ordered_keys):
        logger.debug("preparing output")
        ordered = OrderedDict()

        for key in ordered_keys:
            ordered[key] = output[key]

        return ordered
