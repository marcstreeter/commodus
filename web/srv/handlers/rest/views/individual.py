import logging

from tornado.escape import json_decode
from tornado.web import HTTPError
from voluptuous import (
    All,
    Optional,
    Required,
    Schema,
    REMOVE_EXTRA
)

from ..models import individual as model
from . import BaseView

# schemas
individual_create_schema = Schema(
    {
        # REQUIRED
        Required('individual_id'): All(str, ),
        Required('surname'): All(str, ),
        Required('telephone'): All(str, ),
    },
    extra=REMOVE_EXTRA
)
individual_read_schema = Schema(
    {
        # REQUIRED
        Optional('individual_id'): All(str, ),
    },
    extra=REMOVE_EXTRA
)

logger = logging.getLogger(__name__)


class IndividualView(BaseView):
    async def post(self):
        try:
            kwargs = individual_create_schema(
                json_decode(self.request.body)
            )
        except Exception as e:
            raise HTTPError(
                status_code=400,
                reason=str(e)
            )

        try:
           output = await model.create(
                session=self.session,
                origin_id=kwargs['individual_id'],
                surname=kwargs['surname'],
                telephone=kwargs['telephone']
            )
        except Exception as e:
            raise HTTPError(
                status_code=500,
                reason="failed to store message",
                log_message=f"storing message failed because {e}"
            )

        try:
            self.set_status(201)
            self.write(output)
            self.finish()
        except Exception as e:
            raise HTTPError(500, f"failed to send create output({e})")

    async def get(self, individual_id):
        """
        retrieve guid details

        **Example request**:
        GET /guid/1A9FA24E14F14CD2B4A708A62D4C7F88 HTTP/1.1
        Host: 127.0.0.1:8888
        Connection: close
        User-Agent: Paw/3.1.3 (Macintosh; OS X/10.12.6) GCDHTTPRequest

        **Example response**:
        HTTP/1.1 200 OK
        Server: TornadoServer/4.5.1
        Content-Type: application/json; charset=UTF-8
        Date: Thu, 24 Aug 2017 21:27:32 GMT
        Etag: "60206aa5d167884d548afa7c73fb208f428e43df"
        Content-Length: 93

        {"guid": "1A9FA24E14F14CD2B4A708A62D4C7F88", "expire": "1427736345", "user": "Cylance, Inc."}

        """
        logger.debug("entered get")
        # execute
        try:
            result = await model.read(session=self.session, guid=guid)
        except errors.CylanceErrors:
            raise
        except Exception as e:
            raise HTTPError(500, f"failed to read model({e})")
        else:
            logger.debug("read model")

        # prepare output
        try:
            ordered_keys = ('guid', 'expire', 'user')
            output = self.prepare_output(output=result, ordered_keys=ordered_keys)
        except Exception as e:
            raise HTTPError(500, f"failed to prepare read ouput({e})")
        else:
            logger.debug("read output prepared")

        # send output
        try:
            self.write(output)
            self.finish()
        except Exception as e:
            raise HTTPError(500, f"failed to send read output({e})")
