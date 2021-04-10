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


def get_sanction_level(agent, input_value, action, influence):

    sanction = list(filter(
        lambda x: x if x['action'] == action and x['input_value'] == input_value else False,
        agent.data['sanctions']
    ))

    if len(sanction) > 0 and sanction[0]['level'] > 0:
        sanction_level = abs(sanction[0]['level'] / sum([
            x['level'] for x in agent.data['sanctions']
            if x['input_value'] == input_value
        ]))

        final_influence = sanction_level / influence
        biggest_value = max([sanction_level, influence])
        return [1, final_influence, action, biggest_value]

    else:
        final_influence = influence
        biggest_value = influence
        return [2, final_influence, action, biggest_value]


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
        # memory_coersion = max(outputs) / len(memories)
        memory_coersion = max(outputs) / len(agent.data['memory'])
        return [memory_suggestion, memory_coersion]
    else:
        return None


def closest(lst, K):

    return lst[min(range(len(lst)), key=lambda i: abs(lst[i]-K))]


def order_influence(indexed_influence, field, C):

    differ_list = list(map(
        lambda x: [x[0], abs(C - x[1][field])],
        indexed_influence
    ))

    return sorted(differ_list, key=lambda x: x[-1])
