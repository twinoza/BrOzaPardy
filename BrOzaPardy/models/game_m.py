"""
Model Classes for Game objects
"""
from OzaPardy.models.timer_m import Timer
from OzaPardy.models.team_m import Team
from OzaPardy.models.category_m import Category
from OzaPardy.models.grid_m import Grid

class Game(object):
    def __init__(self, teams, grids, final_category, time_up = 10.):
        """
        :param teams (list): List of Team objects
        :param grids (list): List of first and second round objects
        :param final_category:
        :param time_up (float): seconds allowed to answer each question
        """
        self.teams = teams
        self.teams_hash = {t.name:ind for ind,t in enumerate( teams)}
        self.grids = grids
        self.final_category = final_category

        #instantiate the game
        self.round = 1
        self.active_team =  None
        self.timer =  Timer( time_up)

    def as_dict(self):
        return {"@module": self.__class__.__module__,
                "@class": self.__class__.__name__,
                "teams": [team.as_dict() for team in self.teams],
                "grids": [grid.as_dict() for grid in self.grids],
                "final_category": self.final_category.as_dict()
                }

    @staticmethod
    def from_dict(d):
        teams = [Team.from_dict(tdict) for tdict in d['teams']]
        grids = [Grid.from_dict(gdict) for gdict in d['grids']]
        final_category = Category.from_dict(d['final_category'])
        return Game( teams, grids, final_category)

