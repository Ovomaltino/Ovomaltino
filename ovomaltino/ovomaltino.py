import typing as tp
import random as r
from datetime import datetime
from requests import request, Response
from classes.independent_agent import IndependentAgent
from classes.education import Education
from classes.religion import Religion
from classes.family import Family
from classes.agent import Agent
from classes.collective_conscience import CollectiveConscience
from database.database import Database
from datatype.response_type import ResponseType
from handler.ovomaltino_handler import load_social_facts, load_groups
from handler.group_handler import calculate_action
from handler.mappers import to_agent


class Ovomaltino():

    def __init__(self, api_url: str, api_port: str, api_version: str) -> tp.NoReturn:
        self.api = api_url
        self.port = api_port
        self.version = api_version
        self.url = f'{api_url}:{api_port}/api/{api_version}/'
        self.databases = {'agents': Database(self.url, 'agents'),
                          'consciences': Database(self.url, 'consciences'),
                          'families': Database(self.url, 'families'),
                          'educations': Database(self.url, 'educations'),
                          'religions': Database(self.url, 'religions')}
        self.iagent = IndependentAgent()
        self.conscience = CollectiveConscience('conscience', 3)
        self.family = Family('family', 1)
        self.education = Education('education', 1)
        self.religion = Religion('religion', 1)
        self.groups = []
        self.loadedAt = False

    def load(self, num_groups: int, interactions: tp.Any, responses: tp.List[ResponseType]) -> tp.NoReturn:

        if self.isconnected():
            load_social_facts(self)
            self.groups = load_groups(self, num_groups)
            self.loadedAt = datetime.now().ctime()
            self.num_groups = num_groups
            self.interactions = interactions
            self.responses = responses
        else:
            return "Can't connect in API"

    def reload(self) -> tp.NoReturn:

        if self.loadedAt != False:
            return self.load(self.num_groups, self.interactions, self.responses)
        else:
            return "Ovomaltino wasn't loaded yet"

    def get_leaders(self):

        return list(map(lambda group: group.leader, self.groups))

    def get_learners(self):

        return list(map(lambda group: group.leader, self.groups))

    def get_agent(self, agent_id):

        return Agent(to_agent(self.databases['agents'].get({'_id': agent_id}).json()[0]))

    def process(self, input_value):

        backup = self

        def save():

            self.databases['consciences'].update(self.conscience.data['_id'],
                                                 self.conscience.data)

            self.databases['families'].update(self.family.data['_id'],
                                              self.family.data)

            self.databases['educations'].update(self.education.data['_id'],
                                                self.education.data)

            self.databases['religions'].update(self.religion.data['_id'],
                                               self.religion.data)

            list(map(lambda x: self.databases['agents'].update(x.data['_id'], x.data), list(
                x.leader for x in self.groups
            )))

            list(map(lambda x: self.databases['agents'].update(x.data['_id'], x.data), list(
                x.learner for x in self.groups
            )))

        def rollback():
            return backup

        # os fatos sociais pegam a sua influencia
        education_influence = self.education.influence(input_value)
        religion_influence = self.religion.influence(input_value)
        family_influence = self.family.influence(input_value)
        conscience_influence = self.conscience.influence(input_value)

        # os lideres calculam a sua ação
        actions_suggestion = calculate_action(self, input_value, conscience_influence,
                                              education_influence, family_influence, religion_influence)

        # verifica se há algum número em comum entre os valores passados
        # se sim retorna o mesmo, senão escolhe aleatoriamente
        inputs = list(dict.fromkeys(actions_suggestion))
        outputs = list(len(list(filter(
            lambda y: y == x,
            actions_suggestion
        ))) for x in inputs)

        if max(outputs) > 1:
            return {'response': inputs[outputs.index(max(outputs))],
                    'save': save,
                    'rollback': rollback}

        else:
            return {'response': r.choice(actions_suggestion),
                    'save': save,
                    'rollback': rollback}

    def observe(self, input_value, output_value, old_value, new_value):
        self.education.shape(input_value, output_value, old_value, new_value)
        self.databases['educations'].update(self.education.data['_id'],
                                            self.education.data)

    def consequence(self, value):

        def save():

            self.databases['consciences'].update(self.conscience.data['_id'],
                                                 self.conscience.data)

            self.databases['families'].update(self.family.data['_id'],
                                              self.family.data)

            self.databases['educations'].update(self.education.data['_id'],
                                                self.education.data)

            self.databases['religions'].update(self.religion.data['_id'],
                                               self.religion.data)

            list(map(lambda x: self.databases['agents'].update(x.data['_id'], x.data), list(
                x.leader for x in self.groups
            )))

            list(map(lambda x: self.databases['agents'].update(x.data['_id'], x.data), list(
                x.learner for x in self.groups
            )))

        def apply(agent):
            agent.data['life'] += self.responses[value]['consequence']

        list(map(apply, list(x.leader for x in self.groups)))
        return {'save': save}

    def isconnected(self) -> bool:

        try:
            res: Response = request('GET', self.url)
            return res.status_code == 200
        except:
            return False

    def isloaded(self) -> bool:
        return self.loadedAt != False
