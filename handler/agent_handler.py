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


def upgrade_agent(ovomaltino, learner) -> Agent:

    new_leader_values = {
        'leader': True,
        'becomeLeader': datetime.now().ctime()
    }

    new_leader = Agent(learner.data | new_leader_values)

    ovomaltino.databases['agents'].update(
        new_leader.data['_id'], new_leader.data
    ).json()

    create_new_learner(ovomaltino, new_leader.data['_id'])

    return new_leader


def check_agent(ovomaltino, agent: Agent) -> Agent:

    if agent.data['life'] > 0:
        return agent
    else:
        death_values = {'death': datetime.now().ctime(), 'leader': False}
        agent.data = agent.data | death_values

        ovomaltino.databases['agents'].update(
            agent.data['_id'], agent.data
        ).json()

        return upgrade_agent(ovomaltino, Agent(to_agent(
            ovomaltino.databases['agents'].get(
                filters={'progenitor': agent.data['_id']}).json()[0]
        )))
