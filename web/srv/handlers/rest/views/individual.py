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
from libs import errors

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

    async def get(self, individual_id=None):
        """
        retrieve individual details
        """
        logger.debug("entered get")

        try:  # execute
            output = await model.read(
                session=self.session,
                individual_id=individual_id
            )
        except errors.CommodusErrors:
            raise
        except Exception as e:
            raise HTTPError(500, f"failed to read model({e})")
        else:
            logger.debug("read model")

        try:  # send output
            self.write(output)
            self.finish()
        except Exception as e:
            raise HTTPError(500, f"failed to send read output({e})")
