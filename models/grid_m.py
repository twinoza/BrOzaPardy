"""
Model Classes for Grid objects
"""

class Grid(object):
    def __init__(self, categories, round, daily_doubles = True):
        """
        :param categories (list): list of categories
        :param round: (int 1 or 2): Number of
        :param daily_doubles (bool): Whether to include daily doubles or not
        """
        self.categories = categories
        # self.hash_cats = {cat.title: ind for ind,cat in enumerate( categories)}

        #specify extra daily doubles as needed
        self.daily_doubles = daily_doubles
        if daily_doubles:
            cnt_dd_boxes = 0
            for cat in self.categories:
                if cat.daily_double is not None:
                    cnt_dd_boxes += 1

            if cnt_dd_boxes != round:
                #TODO: do random number generation for any extra daily double required
                #TODO: reinstantiate categories with daily doubles

        # list of which boxes were clicked
        self.is_clicked = [[False for idx in range(5)] for c in range(len(categories))]

    def as_dict(self):
        return {"@module": self.__class__.__module__,
                "@class": self.__class__.__name__,
                "categories": [cat.as_dict() for cat in self.categories],
                "round": self.round,
                "daily_doubles": self.daily_double
                }

    @staticmethod
    def from_dict(d):
        categories = [Category.from_dict(cdict) for cdict in d["categories"]]
        return Grid(categories, d["round"],
                    daily_doubles=d["daily_double"])