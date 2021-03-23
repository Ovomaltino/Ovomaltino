from requests import request
from classes.education import Education
from classes.religion import Religion
from classes.family import Family
from classes.collective_conscience import CollectiveConscience
from database.database import Database
from handler.ovomaltino_handler import check_social_facts


class Ovomaltino():

    def __init__(self, api_url, api_port, api_version):
        self.api = api_url
        self.port = api_port
        self.version = api_version
        self.url = f'{api_url}:{api_port}/{api_version}/'
        self.databases = {'agents': Database(self.url, 'agents'),
                          'iagents': Database(self.url, 'iagents'),
                          'consciences': Database(self.url, 'consciences'),
                          'families': Database(self.url, 'families'),
                          'educations': Database(self.url, 'educations'),
                          'religions': Database(self.url, 'religions')}
        self.iagent = False
        self.conscience = CollectiveConscience('conscience', 3)
        self.family = Family('family', 1)
        self.education = Education('education', 1)
        self.religion = Religion('religion', 1)
        self.agents = []
        self.loaded = False

    def load(self, num_groups, interactions, responses):

        if self.isconnected():
            pass
        else:
            return "Can't connect in API"

        [check_social_facts(sf, db)
         for sf in [self.family, self.education, self.religion, self.conscience]
         for db in [self.databases['families'], self.databases['educations'],
                    self.databases['religions'], self.databases['consciences']]]

    def process(self):
        pass

    def observe(self):
        pass

    def consequences(self):
        pass

    def isconnected(self):

        try:
            res = request('GET', self.url)
            return res.status_code == 200
        except:
            False

    def isloaded(self):
        return self.loaded == True
