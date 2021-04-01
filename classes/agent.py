import random as r
from handler.agent_handler import get_myself_data, get_sanction_level, closest


class Agent():

    def __init__(self, data):
        self.data = data

    def act(self, input_value, interactions, education, religion, conscience, family):

        myself = get_myself_data(self, input_value, interactions)
        filter_conscience = [
            r.choice(conscience[0]), conscience[1]] if conscience is not None else None
        results = [[abs(x[1] / get_sanction_level(self, x[0])), x[0]]
                   for x in [myself, religion, education, family, filter_conscience] if x is not None]

        biggest_influence = closest([x[0] for x in results], 1)
        action = list(filter(
            lambda x: x[0] == biggest_influence, results
        ))

        self.data['memory'] = self.data['memory'] + [{
            'isLearner': False,
            'inputValue': input_value,
            'action': action[0][1]
        }]

        return action[0][1]

    def learn(self, leader, leader_action, education, input_value):

        leader_data = [leader_action, 1 - len(
            self.data['memory']) / len(leader.data['memory'])]

        if education is None:
            self.data['memory'] = self.data['memory'] + [{
                'isLearner': True,
                'inputValue': input_value,
                'action': leader_action
            }]

        elif leader_data[1] / education[1] > 1:
            self.data['memory'] = self.data['memory'] + [{
                'isLearner': True,
                'inputValue': input_value,
                'action': leader_action
            }]
        else:
            self.data['memory'] = self.data['memory'] + [{
                'isLearner': True,
                'inputValue': input_value,
                'action': education[0]
            }]
