from typing import NoReturn
from classes.social_fact import SocialFact
from database.database import Database
from handler.mappers import to_social_fact


def check_social_facts(sf: SocialFact, db: Database) -> NoReturn:

    if sf.data == False:

        res = db.get(offset=0, limit=1).json()

        if len(res) == 1:
            sf.data = to_social_fact(res)
        else:
            sf.register(db, {})

    else:
        pass
