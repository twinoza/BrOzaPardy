"""
Model Classes for Team objects
"""

class Team(object):
    def __init__(self, name):
        """
        :param name (str):
        """
        self.name = name
        self.score = 0
        self.score_history = [self.score]

    def update_score(self, value):
        self.score += value
        self.score_history.append( self.score) #TODO: store time?

    def as_dict(self):
        return {"@module": self.__class__.__module__,
                "@class": self.__class__.__name__,
                "name": self.name}

    @staticmethod
    def from_dict(d):
        return Team(d['name'])

