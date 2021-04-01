from abc import ABC, abstractmethod
from database.database import Database
from datatype.social_fact_type import SocialFactType
from handler.mappers import to_social_fact


class SocialFact(ABC):

    def __init__(self, name: str, sanction_level: int) -> bool:
        self.name = name
        self.sanction_level = sanction_level
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

    def sanction(self, agents, influence, actions):

        def apply(agent, action):

            if influence[0] == action:
                check_sanction = list(filter(
                    lambda x: x['action'] == action,
                    agent.data['sanctions']
                ))

                if len(check_sanction) > 0:
                    for sanction in iter(agent.data['sanctions']):
                        if sanction['action'] == action and sanction['level'] > 0:
                            sanction['level'] -= self.sanction_level

                else:
                    pass

            else:
                check_sanction = list(filter(
                    lambda x: x['action'] == action,
                    agent.data['sanctions']
                ))

                if len(check_sanction) > 0:
                    for sanction in iter(agent.data['sanctions']):
                        if sanction['action'] == action and sanction['level'] > 0:
                            sanction['level'] += self.sanction_level
                else:
                    agent.data['sanctions'] = agent.data['sanctions'] + [{
                        'action': action,
                        'level': self.sanction_level
                    }]

        if influence is not None:
            list(map(apply, agents, actions))
        else:
            pass

    @abstractmethod
    def shape(self, input_value, output_value):
        pass

    @abstractmethod
    def influence(self, input_value):
        pass
