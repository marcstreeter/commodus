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

from ..models import twilio as model
from . import BaseView

# schemas
status_update_schema = Schema(
    {
        # REQUIRED
        Required('MessageSid'): All(str, ),
        Required('From'): All(str, ),
        Required('To'): All(str, ),
        Required('Body'): All(str, ),
        Optional('MessageStatus'): All(str, ),
        Optional('ErrorCode'): All(str, ),

        # IGNORED
        # 'MessagingServiceSid'
        # 'SmsSid'  # DEPRECATED
        # 'AccountSid'
        # 'NumMedia'
        # 'FromCity'
        # 'FromState'
        # 'FromZip'
        # 'FromCountry'
        # 'ToCity'
        # 'ToState'
        # 'ToZip'
        # 'ToCountry'
        # 'MediaContentType{N}'
        # 'MediaUrl{N}'
    },
    extra=REMOVE_EXTRA
)

logger = logging.getLogger(__name__)


class TwilioView(BaseView):
    async def post(self):
        try:
            kwargs = status_update_schema(
                json_decode(self.request.body)
            )
        except Exception as e:
            raise HTTPError(
                status_code=400,
                reason=str(e)
            )

        try:
            await model.upsert(
                session=self.session,
                twilio_message_id=kwargs['MessageSid'],
                body=kwargs['Body'],
                from_number=kwargs['From'],
                to_number=kwargs['To'],
                status=kwargs.get('MessageStatus'),
                code=kwargs.get('ErrorCode')
            )
        except Exception as e:
            raise HTTPError(
                status_code=500,
                reason="failed to store message",
                log_message=f"storing message failed because {e}"
            )

        # send output
        self.set_status(204)
        self.finish()