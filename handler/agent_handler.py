from datetime import datetime
from classes.agent import Agent
from datatype.agent_type import AgentType
from handler.mappers import to_agent


def create_new_leader(ovomaltino) -> AgentType:

    return Agent(to_agent(ovomaltino.databases['agents'].create({
        'birth': datetime.now().ctime(),
        'progenitor': "I'm the first one, guy",
        'leader': True,
        'becomeLeader': datetime.now().ctime(),
        'life': 100,
        'memory': [],
        'sanctions': [],
        'actions': 0
    }).json()))


def create_new_learner(ovomaltino, leader_id) -> AgentType:

    return Agent(to_agent(ovomaltino.databases['agents'].create({
        'birth': datetime.now().ctime(),
        'progenitor': leader_id,
        'leader': False,
        'life': 100,
        'memory': [],
        'sanctions': [],
        'actions': 0
    }).json()))
