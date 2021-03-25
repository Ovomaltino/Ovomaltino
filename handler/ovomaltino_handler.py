import operator as op
import typing as tp
from classes.groups import Group
from classes.agent import Agent
from classes.social_fact import SocialFact
from database.database import Database
from handler.mappers import to_social_fact, to_agent
from handler.group_handler import create_new_group, fill_group


def load_social_facts(ovomaltino) -> tp.NoReturn:

    def check_social_facts(sf: tp.Tuple[int, SocialFact], dbs: tp.List[Database]) -> tp.Union[SocialFact, tp.Callable]:

        if sf[1].data == False:

            res = dbs[sf[0]].get(offset=0, limit=1).json()

            if len(res) == 1:
                sf[1].data = to_social_fact(res[0])
            else:
                sf[1].register(dbs[sf[0]], {
                    'name': sf[1].name,
                    'moral': [],
                    'sanction_level': sf[1].sanction
                })

        else:
            pass

    dbs = [ovomaltino.databases['families'], ovomaltino.databases['educations'],
           ovomaltino.databases['religions'], ovomaltino.databases['consciences']]

    [check_social_facts(sf, dbs)
     for sf in enumerate([ovomaltino.family, ovomaltino.education, ovomaltino.religion, ovomaltino.conscience])]


def load_groups(ovomaltino, num_groups: int) -> tp.NoReturn:

    try:
        res = ovomaltino.databases['agents'].get(
            filters={'leader': True},
            offset=0,
            limit=num_groups
        ).json()

        if len(res) == num_groups:
            return [fill_group(ovomaltino, Agent(to_agent(x))) for x in res]
        else:
            partial_groups = [fill_group(ovomaltino, Agent(to_agent(x)))
                              for x in res]
            new_groups = [create_new_group(ovomaltino)
                          for x in range(0, num_groups - len(res))]
            return op.add(partial_groups, new_groups)

    except:
        raise SystemError
