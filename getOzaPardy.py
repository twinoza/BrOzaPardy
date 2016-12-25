""" This module provides all the methods in order to:
    'gets' the clues and responses from a TSV file
"""

import g
from numpy import loadtxt
from math import ceil
import random
import opHelperFns as ophf

#Pass in Boxes to be populated
def getJeopardyData(modeType, docName):
    '''Gets the OzaPardy data from a TSV file and stores it into a list of
    ozaPardyBox objects

    Inputs: 
        modeType:   (str) Determines 'Single', 'Double', or 'Final' jeopardy
        docName:    (str) Specify the document name from which to load data

    Return:
        board:      (tuple) ozaPardyBox(es) populated with clues/responses and all
        
    '''
    if modeType == 'Single':
        tmpBoard = g.sBoard
    elif modeType == 'Double':
        tmpBoard = g.dBoard
    elif modeType == 'Final':
        tmpBoard = g.fBoard
    else:
        print("Check your modeType b/c it ain't one I know: " + modeType)

    print("Start getJeopardyData: " + modeType)
    
    data = loadtxt(docName, dtype=bytes, delimiter='\t', skiprows=1).astype(str)
    print('Loaded ' + modeType + ' Jeopardy from ' + docName)
    
    for rowNum, row in enumerate(data):
        for colNum, boxVal in enumerate(row):
            boxNum = int((ceil(rowNum/2.)*6) + (colNum-1))
            if modeType in ['Single', 'Double'] and colNum != 0:
                if rowNum == 0:   # Fill in category Names
                    tmpBoard[boxNum] = boxVal
                else:         # Fill in Clue/Response boxes in board
                    parseOzaPardyBox(tmpBoard[boxNum], boxVal, row[0])
            elif modeType == 'Final':
                if rowNum == 0:
                  tmpBoard[0] = boxVal
                if rowNum == 1:
                  tmpBoard[1].clue = ophf.myWrap(boxVal)
                if rowNum == 2:
                  tmpBoard[1].response = ophf.myWrap(boxVal)

    # Make daily doubles
    if modeType == 'Single':
        r1 = random.randrange(30)
        g.boards[0][r1+6].isDailyDouble = True
    elif modeType == 'Double':
        r2 = random.randrange(30)
        r3 = random.randrange(30)
        while r2 == r3:
            r3 = random.randrange(30)
        
        g.boards[1][r2+6].isDailyDouble = True
        g.boards[1][r3+6].isDailyDouble = True

    return tmpBoard


# opBox is OzaPardyBox
# cellData is the first column of the spreadsheet which determines whether
#     the row is a clue or a response and the point value associated with 
#     that row.
def parseOzaPardyBox(opBox, boxVal, cellData):
    mediaDir = 'static/data/media/'
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
        opBox.clue = ophf.myWrap(clue)
    else:
        opBox.response = ophf.myWrap(clue)

    return opBox

