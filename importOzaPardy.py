from numpy import loadtxt
from math import ceil

#Pass in Boxes to be populated
def getJeopardyData(boxes, gameType=0, doc_name="OzaPardy"):
    print("Start getJeopardyData")

    if gameType == 0:
        fName = 'static/data/OzaPardy - Single.tsv'
        data = loadtxt(fName, dtype='S', delimiter='\t', skiprows=1)
        print('Loaded Single Jeopardy')
    elif gameType == 1:
        fName = 'static/data/OzaPardy - Single.tsv'
        data = loadtxt(fName, dtype='S', delimiter='\t', skiprows=1)
        print('Loaded Double Jeopardy')
    else:
        print('Error in getJeopardyData: Invalid gameType')
        return()
    
    for rowNum, row in enumerate(data):
        for colNum, boxVal in enumerate(row):
            boxNum = int((ceil(rowNum/2.)*6) + (colNum-1))
            if colNum != 0:
                if rowNum == 0:   # Fill in category Names
                    ###boxes[gameType][boxNum] = boxVal #row[key].text
                    print(boxVal)
                else:         # Fill in Clue/Response boxes
                    parseOzaPardyBox(boxes[gameType][boxNum], boxVal, row[0])

# opBox is OzaPardyBox
# cellData is the first column of the spreadsheet which determines whether
#     the row is a clue or a response and the point value associated with 
#     that row.
def parseOzaPardyBox(opBox, boxVal, cellData):
    #[cellType, cellVal] = gDict['tiles'].text.split()
    [cellType, cellVal] = cellData.split()
    opBox.value = cellVal

    parsedMediaType = ''
    clue = boxVal

    if '<>' in boxVal:
        parsedMediaType, parsedMediaFName, clue = boxVal.split('<>')
    if cellType=="Clue":
        if parsedMediaType == 'Img':
            opBox.mediaType = 1
            opBox.mediaFName = mediaDir + parsedMediaFName
        elif parsedMediaType == 'Aud':
            opBox.mediaType = 2
            opBox.mediaFName = mediaDir + parsedMediaFName
        elif parsedMediaType == 'Vid':
            opBox.mediaType = 3
            opBox.mediaFName = mediaDir + parsedMediaFName
        opBox.clue = self.myWrap(clue)
    else:
        opBox.response = self.myWrap(clue)
