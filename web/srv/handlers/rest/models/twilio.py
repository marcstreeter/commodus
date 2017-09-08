import logging
import uuid

from libs.db import Query
from libs.individual import get_or_create_individual


logger = logging.getLogger(__name__)


async def upsert(session, twilio_message_id, body, to_number, from_number, status=None, code=None):
    """
    updates or inserts
    :param session: database session within request context
    :param twilio_message_id:
    :param body:
    :param from_number:
    :param to_number:
    :param status:
    :param code:
    :return:
    """
    # check for existing twilio message to update

    if await twilio_message_exists(session, twilio_message_id):
        # update status/error
        # if no status/error supplied raise stink
        # else set
        params = {}
        clauses = []

        if not status and not code:
            logger.warning(
                "skipping message update because neither status nor code supplied"
            )
            return

        if status is not None:
            params['status'] = status
            clauses.append("status = %(status)s")

        if code is not None:
            params['code'] = code
            clauses.append("error_code = %(code)s")

        clauses = ','.join(clauses)
        sql = (
            "UPDATE twilio_message "
            f"SET {clauses} "
            "WHERE twilio_message_id = %(tmsid)s"
        )

        async with Query(session=session, sql=sql, params=params):
            # TODO find a way to confirm went through properly
            pass
    else:
        from_individual_id = await get_or_create_individual(
            session=session,
            origin='twilio.com',
            telephone_number=from_number
        )
        to_individual_id = await get_or_create_individual(
            session=session,
            origin='twilio.com',
            telephone_number=to_number
        )
        message_id = await create_message(
            session=session,
            body=body,
            sender=from_individual_id,
            receiver=to_individual_id
        )

        await create_twilio_message(
            session=session,
            twilio_message_id=twilio_message_id,
            message_id=message_id,
            from_number=from_number,
            to_number=to_number
        )

    # TODO notify watchers

async def twilio_message_exists(session, twilio_message_id):
    params = {
        'tmsgid': twilio_message_id
    }
    sql = (
        "SELECT * "
        "FROM twilio_message "
        "WHERE twilio_message_id = %(tmsgid)s"
    )

    async with Query(session=session, sql=sql, params=params) as results:
        return results.count() is 1



async def create_message(session, body, receiver, sender):
    # create new message
    message_id = str(uuid.uuid4()).replace('-', '')
    params = {
        'message_id': message_id,
        'body': body,
        'sender': sender,
        'receiver': receiver
    }
    sql = (
        "INSERT INTO message (message_id, body, sender, receiver) "
        "VALUES (%(message_id)s, %(body)s, %(sender)s, %(receiver)s)"
    )

    async with Query(session=session, sql=sql, params=params):
        # TODO do something to confirm that was ran successfully
        pass

    return message_id

async def create_twilio_message(session, twilio_message_id, message_id, from_number, to_number):
    params = {
        'tmid': twilio_message_id,
        'msgid': message_id,
        'from': from_number,
        'to': to_number
    }
    sql = (
        'INSERT INTO twilio_message (twilio_message_id, message_id, "from", "to") '
        'VALUES (%(tmid)s, %(msgid)s, %(from)s, %(to)s) '
    )

    async with Query(session=session, sql=sql, params=params):
        # TODO do something to confirm that was ran successfully
        pass

    return

