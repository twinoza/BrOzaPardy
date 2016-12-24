class ozaPardyBox(object):
    def __init__(self, boxId, clue=None, response=None, value=None, isClicked=False,
                 isDailyDouble=False, isAnswered=False, mediaType=0, mediaFName=''):
        self.id = boxId
        self.clue = clue
        self.response = response
        self.value = value
        self.isClicked = isClicked
        self.isDailyDouble = isDailyDouble
        self.isAnswered = isAnswered

        # 0 = Text (i.e. Not Media), 1 = Image, 2 = Audio, 3 = Video 
        self.mediaType = mediaType
        self.mediaFName = 'media/'+mediaFName


    def clicked(self):
        self.isClicked = True


class team(object):
    def __init__(self, teamId, name, score=0):
        self.id = teamId
        self.name = name
        self.score = score
        #Maybe include way to track right and wrong answers
