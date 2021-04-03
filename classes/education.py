import operator as op
from classes.social_fact import SocialFact


class Education(SocialFact):

    def shape(self, input_value, output_value, old_value, new_value):

        def change(test_value):
            if test_value == old_value:
                return new_value
            elif test_value == new_value:
                return old_value
            else:
                return test_value

        new_input_value = list(map(change, input_value))
        new_moral = {'inputValue': new_input_value,
                     'outputValue': output_value}

        self.data['moral'] = op.add(self.data['moral'], [new_moral])

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
