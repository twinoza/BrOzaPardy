"""
Model Classes for Category objects
"""

class Category(object):
    def __init__(self, boxes, title, daily_double=None):
        """

        :param boxes (list): Final jeopardy only has one item in a list.
            All others have exactly five boxes
        :param title (str): Name of category
        :param daily_double (int or None): Box list index for daily double.
            options are:
                        None = No daily double in this category
                        <int> = Daily double for int value
        """
        if len(boxes) not in [1,5]:
            #TODO: more value errors for not being a box etc.
            raise ValueError("Not a list of five boxes!")
        self.boxes = boxes
        # self.hash_boxes = {box.clue: ind for ind,box in enumerate( boxes)}
        self.title = title

        if isinstance(daily_double, int):
            self.daily_double = daily_double
        elif len(boxes) == 1:
            self.daily_double = 0
        elif daily_double is not None:
            raise ValueError("daily_double = {} (instance {}) not recognized"
                             "".format(daily_double, type(daily_double)))
        else:
            self.daily_double = None

    def as_dict(self):
        return {"@module": self.__class__.__module__,
                "@class": self.__class__.__name__,
                "boxes": [box.as_dict() for box in self.boxes],
                "title": self.title,
                "daily_double": self.daily_double
                }

    @staticmethod
    def from_dict( d):
        boxes = [Box.from_dict(bdict) for bdict in d["boxes"]]
        return Category( boxes, d["title"],
                         daily_double = d["daily_double"])

