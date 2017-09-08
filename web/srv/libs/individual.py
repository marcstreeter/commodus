import logging
import uuid

from .db import Query

logger = logging.getLogger(__name__)

async def get_or_create_individual(session, origin, telephone_number, surname=None, origin_id=None):
    # check all individuals for telephone
    # if more than one individual exists with telephone number
    #     look for individual who was most recent to receive or transmit a message
    # elif one individual exists
    #     assign telephone message to this individual
    # else (doesn't map to anyone)
    #     assign anonymous

    # TODO - extract details from callerid?
    # TODO - extract from message details from text that indicate who it is (machine learning)

    # select existing
    params = {
        'telephone': telephone_number,
    }
    sql = """
            SELECT individual_id
            FROM individual 
            WHERE telephone = %(telephone)s
            ORDER BY last_activity DESC LIMIT 1
    """

    async with Query(session=session, sql=sql, params=params) as results:
        try:
            individual_id = [i for i in results]['individual_id']
        except:
            logger.debug("no existing individual with that phone number")
        else:
            logger.debug("found existing individual")
            return individual_id

    # create new
    logger.debug("creating individual entry...")
    individual_id = str(uuid.uuid4()).replace('-', '')
    params = {
        'individual_id': individual_id,
        'origin_id': origin_id,
        'surname': surname,
        'telephone': telephone_number,
        'origin': origin
    }

    sql = (
        "INSERT INTO individual (individual_id, surname, telephone, origin, origin_id) "
        "VALUES (%(individual_id)s, %(surname)s, %(telephone)s, %(origin)s, %(origin_id)s)"
    )

    async with Query(session=session, sql=sql, params=params):
        # TODO do something to confirm that was ran successfully
        pass

    return individual_id

async def individual_exists(session, **filters):
    params = {}
    if 'individual_id' in filters:
        params['individual_id'] = filters['individual_id']

    if 'origin_id' in filters:
        params['origin_id'] = filters['origin_id']

    clauses = ' AND '.join(
        f"{key} = %({key})s" for key in params.keys()
    )

    sql = (
        "SELECT * "
        "FROM individual "
        f"WHERE {clauses}"
    )

    async with Query(session=session, sql=sql, params=params) as results:
        return results.count() is 1

async def recent_updates_exist(session):
    pass
