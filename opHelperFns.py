""" This module contains all the methods that are useful to have, but do not
    require any ozaPardy specific classes.

    These methods are required by some ozaPardy files in order to function
"""

import textwrap

def myWrap(inStr):
    ''' Wraps text

        Inputs:
            inStr:  (str) Input text that needs to be wrapped

        Return:
            outStr: (str) Modified text with '\n' to automatically wrap text
    '''
    outStr = textwrap.wrap(inStr, 30)
    outStr = '\n'.join(outStr) 
    return outStr

def gmMode(modeType="Single"):
    ''' Translates the current game mode to a number:
            Single   : 0
            Double   : 1
            Final    : 3
            Clue     : 4
            Klok     : 5
            Response : 6
            Daily    : 7
            Blank    : 8

        Inputs:
            modeType:   (str) Current game mode
            
        Return:
            rdNum:      (int) Corresponding number of game mode
    '''
    
    modes = ['Single', 'Double', 'Final', 'Clue',
             'Klok', 'Response', 'Daily', 'Blank']

    if modeType in modes:
      return modes.index(modeType)
    else: return 0

def boxNum2boxId(num):
    ''' Converts the boxNum for any given box to its respective column and row
        coded as an ID (= 10*col + row)

        Input:
            num:    (int) Between 6 and 35 that represents the List Index

        Return:
            boxId:  (int) ID for the ozaPardyBox that indicates col and row

         0 : C1      1 : C2      2 : C3      3 : C4      4 : C5      5 : C6
         6 : 11      7 : 21      8 : 31      9 : 41     10 : 51     11 : 61
        12 : 12     13 : 22     14 : 32     15 : 42     16 : 52     17 : 62
        18 : 13     19 : 23     20 : 33     21 : 43     22 : 53     23 : 63
        24 : 14     25 : 24     26 : 34     27 : 44     28 : 54     29 : 64
        30 : 15     31 : 25     32 : 35     33 : 45     34 : 55     35 : 65
    '''
    cr = [(cc+1)*10+rr+1 for rr in range(5) for cc in range(6)]
    lookup = {kk:vv for kk,vv in zip(range(6,36), cr)}
    if num in lookup.keys():
        return lookup[num]
    else:
        return -1

def boxId2boxNum(boxId):
    ''' Converts the boxId for any given box to its respective list index
        referred to as boxNum

        Input:
            boxId:    (int) ID for the ozaPardyBox that indicates col and row

        Return:
            boxNum:   (int) Between 6 and 35 that represents the List Index

         0 : C1      1 : C2      2 : C3      3 : C4      4 : C5      5 : C6
         6 : 11      7 : 21      8 : 31      9 : 41     10 : 51     11 : 61
        12 : 12     13 : 22     14 : 32     15 : 42     16 : 52     17 : 62
        18 : 13     19 : 23     20 : 33     21 : 43     22 : 53     23 : 63
        24 : 14     25 : 24     26 : 34     27 : 44     28 : 54     29 : 64
        30 : 15     31 : 25     32 : 35     33 : 45     34 : 55     35 : 65
    '''
    cr = [(cc+1)*10+rr+1 for rr in range(5) for cc in range(6)]
    lookup = {kk:vv for vv,kk in zip(range(6,36), cr)}
    if boxId in lookup.keys():
        return lookup[boxId]
    else:
        return -1
