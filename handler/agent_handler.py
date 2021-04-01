import random as r
from datetime import datetime
from datatype.agent_type import AgentType
from handler.mappers import to_agent


def create_new_leader(ovomaltino) -> AgentType:

    return to_agent(ovomaltino.databases['agents'].create({
        'birth': datetime.now().ctime(),
        'progenitor': "I'm the first one, guy",
        'leader': True,
        'becomeLeader': datetime.now().ctime(),
        'life': 100,
        'memory': [],
        'sanctions': [],
        'actions': 0
    }).json())


def create_new_learner(ovomaltino, leader_id) -> AgentType:

    return to_agent(ovomaltino.databases['agents'].create({
        'birth': datetime.now().ctime(),
        'progenitor': leader_id,
        'leader': False,
        'life': 100,
        'memory': [],
        'sanctions': [],
        'actions': 0
    }).json())


def upgrade_agent(ovomaltino, learner):

    new_leader_values = {
        'leader': True,
        'becomeLeader': datetime.now().ctime()
    }

    new_leader = learner.data | new_leader_values

    ovomaltino.databases['agents'].update(
        new_leader['_id'], new_leader
    ).json()

    create_new_learner(ovomaltino, new_leader['_id'])
    return new_leader


def check_agent(ovomaltino, agent):

    if agent.data['life'] > 0:
        return agent
    else:
        death_values = {'death': datetime.now().ctime(), 'leader': False}
        agent.data = agent.data | death_values

        ovomaltino.databases['agents'].update(
            agent.data['_id'], agent.data
        ).json()

        return upgrade_agent(ovomaltino, to_agent(
            ovomaltino.databases['agents'].get(
                filters={'progenitor': agent.data['_id']}).json()[0]
        ))


def get_sanction_level(agent, action):

    sanction = list(filter(
        lambda x: x if x['action'] == action else False,
        agent.data['sanctions']
    ))

    if len(sanction) > 0 and sanction[0]['level'] > 0:
        return sanction[0]['level'] / sum([x['level'] for x in agent.data['sanctions']])
    else:
        return 1


def get_myself_data(agent, input_value, interactions):

    memories = list(x['action'] for x in filter(
        lambda x: x if x['inputValue'] == input_value else False,
        agent.data['memory']
    ))

    if len(memories) > 0:
        inputs = list(dict.fromkeys(memories))
        outputs = list(len(list(filter(
            lambda y: y == x,
            memories
        ))) for x in inputs)

        memory_suggestion = inputs[outputs.index(max(outputs))]
        memory_coersion = max(outputs) / sum(outputs)
    else:
        memory_suggestion = memory_coersion = None

    intuition_suggestion = r.choice(interactions)
    intuition_coersion = r.uniform(0, 1)

    if memory_coersion is not None and memory_coersion / intuition_coersion > 1:
        return [memory_suggestion, memory_coersion]
    else:
        return [intuition_suggestion, intuition_coersion]


def closest(lst, K):

    return lst[min(range(len(lst)), key=lambda i: abs(lst[i]-K))]
