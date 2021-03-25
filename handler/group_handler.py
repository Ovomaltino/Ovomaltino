from datatype.group_type import GroupType
from datatype.agent_type import AgentType
from classes.agent import Agent
from classes.groups import Group
from handler.mappers import to_agent
from handler.agent_handler import create_new_leader, create_new_learner


def create_new_group(ovomaltino) -> GroupType:

    leader = create_new_leader(ovomaltino)
    learner = create_new_learner(ovomaltino, leader.data['_id'])
    return Group(leader, learner)


def fill_group(ovomaltino, leader: AgentType) -> Group:

    return Group(leader, Agent(to_agent(ovomaltino.databases['agents'].get(filters={'progenitor': leader.data['_id']}).json()[0])))
