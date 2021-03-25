from abc import ABC, abstractmethod
from database.database import Database
from datatype.social_fact_type import SocialFactType
from handler.mappers import to_social_fact


class SocialFact(ABC):

    def __init__(self, name: str, sanction_level: int) -> bool:
        self.name = name
        self.sanction = sanction_level
        self.data = False

    def iscreated(self, db: Database) -> bool:

        try:
            res = db.get(sort='createdAt:desc', offset=0, limit=1).json()
            return len(res) == 1
        except:
            return False

    def register(self, db: Database, obj: SocialFactType) -> bool:

        try:
            self.data = to_social_fact(db.create(obj).json())
            return True
        except:
            return False
