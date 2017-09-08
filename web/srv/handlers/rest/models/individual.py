import logging
import uuid

from libs.db import Query
from libs.individual import (
    individual_exists,
    get_or_create_individual
)

from libs.errors import InvalidRequest

logger = logging.getLogger(__name__)

class Individual:
    def __init__(self, individual_id, surname, telephone, origin_id, origin):
        self.individual_id = individual_id
        self.surname = surname
        self.telephone = telephone
        self.origin_id = origin_id
        self.origin = origin

    def serialize(self):
        return {
            "individual_id": self.individual_id,
            "surname": self.surname,
            "telephone": self.telephone,
            "origin_id": self.origin_id,
            "origin ": self.origin
        }


async def create(session, surname, telephone, origin_id):
    if await individual_exists(
            session=session,
            origin_id=origin_id,
            origin="lds.org"
    ):
        raise InvalidRequest(
            reason="individual already exists with that origin id"
        )
    else:

        individual_id = await get_or_create_individual(
            session=session,
            telephone_number=telephone,
            origin_id=origin_id,
            origin="lds.org"
        )
        return Individual(
            telephone=telephone,
            origin_id=origin_id,
            origin="lds.org",
            individual_id=individual_id,
            surname=surname
        ).serialize()
