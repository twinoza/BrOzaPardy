"""
Model Classes for Box objects
"""

class Box(object):
    def __init__(self, clue, solution, level):
        """
        :param clue:
        :param solution:
        :param level (int 1 - 5): Level value for time
        """
        self.clue = clue
        self.solution = solution
        self.level = level

    def as_dict(self):
        return {"@module": self.__class__.__module__,
                "@class": self.__class__.__name__,
                "clue": self.clue,
                "solution": self.solution,
                "level": self.level
                }

    @staticmethod
    def from_dict( d):
        return Box( d["clue"], d["solution"], d["level"])


class TextBox(Box):

    @staticmethod
    def load_from_file( file_name, format="txt"):
        #TODO: define text clue, solution and level from file_name in format type
        if format == 'txt':
            # xxxx
            return TextBox( clue, solution, level)



"""
TODO (box related): 
    - create Box subclasses for AudioBox, VideoBox, ImageBox
    - for each one, create static methods for instantiation from file types
"""