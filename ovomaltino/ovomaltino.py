import typing as tp
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

    def process(self):
        pass

    def observe(self):
        pass

    def consequences(self):
        pass

    def isconnected(self) -> bool:

        try:
            res: Response = request('GET', self.url)
            return res.status_code == 200
        except:
            return False

    def isloaded(self) -> bool:
        return self.loadedAt != False
