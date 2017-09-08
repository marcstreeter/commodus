from tornado.web import RequestHandler
from tornado.web import HTTPError


class NotFoundView(RequestHandler):
    async def prepare(self):
        """
        default 404 for nonexistent endpoints
        :return:
        """
        raise HTTPError(404, "nothing here")