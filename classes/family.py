import operator as op
from classes.social_fact import SocialFact


class Family(SocialFact):

    def shape(self, input_value, output_value):

        outputs = list(dict.fromkeys(output_value))
        new_morals = list(map(lambda out: {'inputValue': input_value, 'outputValue': out},
                              outputs))

        for moral in iter(new_morals):
            self.data['moral'] = op.add(self.data['moral'], [moral])

    def influence(self, input_value):

        filter_list = list(x['outputValue'] for x in filter(
            lambda x: x if x['inputValue'] == input_value else False,
            self.data['moral']
        ))

        if len(filter_list) > 0:
            inputs = list(dict.fromkeys(filter_list))
            outputs = list(len(list(filter(
                lambda y: y == x,
                filter_list
            ))) for x in inputs)

            suggestion = inputs[outputs.index(max(outputs))]
            coersion = max(outputs) / len(self.data['moral'])
            return (suggestion, coersion)
        else:
            return None
