import operator as op
import functools as ftls
from classes.social_fact import SocialFact


class CollectiveConscience(SocialFact):

    def shape(self, input_value, output_value):

        outputs = sorted(list(dict.fromkeys(output_value)))
        new_moral = {'inputValue': input_value,
                     'outputValue': outputs}

        self.data['moral'] = op.add(self.data['moral'], [new_moral])

    def influence(self, input_value):

        filter_list = list(x['outputValue'] for x in filter(
            lambda x: x if x['inputValue'] == input_value else False,
            self.data['moral']
        ))

        if len(filter_list) > 0:
            inputs = list(dict.fromkeys(''.join(map(str, x))
                                        for x in filter_list))

            outputs = list(len(list(filter(
                lambda y: ''.join(map(str, y)) == x,
                filter_list
            ))) for x in inputs)

            suggestion = list(map(int, inputs[outputs.index(max(outputs))]))
            coersion = max(outputs) / len(filter_list)
            return (suggestion, coersion)
        else:
            return None

    def sanction(self, agents, input_value, influence, actions):

        def apply(agent, action):

            if action in influence[0]:
                check_sanction = list(filter(
                    lambda x: x['action'] == action and x['input_value'] == input_value,
                    agent.data['sanctions']
                ))

                if len(check_sanction) > 0:
                    for sanction in iter(agent.data['sanctions']):
                        if sanction['action'] == action and sanction['input_value'] == input_value and sanction['level'] > 0 and sanction['level'] - self.sanction_level > 0:
                            sanction['level'] -= self.sanction_level

                        elif sanction['action'] == action and sanction['input_value'] == input_value and sanction['level'] > 0 and sanction['level'] - self.sanction_level < 0:
                            sanction['level'] = 0

                        else:
                            pass

                else:
                    pass

            else:
                check_sanction = list(filter(
                    lambda x: x['action'] == action and x['input_value'] == input_value,
                    agent.data['sanctions']
                ))

                if len(check_sanction) > 0:
                    for sanction in iter(agent.data['sanctions']):
                        if sanction['action'] == action and sanction['input_value'] == input_value and sanction['level'] > 0:
                            sanction['level'] += self.sanction_level
                else:
                    agent.data['sanctions'] = agent.data['sanctions'] + [{
                        'input_value': input_value,
                        'action': action,
                        'level': self.sanction_level
                    }]

        if influence is not None:
            list(map(apply, agents, actions))
        else:
            pass
