#!/usr/bin/python

'''
Program: OzaPardy.py (originally named Jeopardy.py)
Author:  Norm Oza, Nick Oza, Neal Oza
Date:  Started Dec 16, 2012

Started: Dec 16, 2012
Dec 24th 2013:  Fixed bugs to actually make it work.
Dec 23rd 2014:  Add in comments and clear up code for media ability
'''
#test
import sys
#import gdata.docs
#import gdata.docs.service
#import gdata.spreadsheet.service
import gspread
import re, os
import time
import datetime as dt
import serial
from math import *

import wx
import wx.media
import wx.lib.buttons as buttons
#import wx.lib.wordwrap
#import wx.lib.wordwrap as wwrap
import textwrap
import random
import Image
#APP_EXIT = 1
from numpy import loadtxt

import argparse
from oauth2client.client import OAuth2WebServerFlow, SignedJwtAssertionCredentials
from oauth2client import tools
from oauth2client.tools import run_flow
from oauth2client.file import Storage
import json


def authorizeOzaPardy():
  print("Authorizing OzaPardy Access")
#  CLIENT_ID = '531072861739-j5v60k5ggpk9h758fm1v6rhktpqdja38.apps.googleusercontent.com'
#  CLIENT_SECRET = 'Fg43Hk6zXw7_aV8_aRGzeXhK'
#
#  flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
#
#  flow = OAuth2WebServerFlow(
#      client_id = CLIENT_ID,
#      client_secret = CLIENT_SECRET,
#      scope = 'https://spreadsheets.google.com/feeds https://docs.google.com/feeds',
#      redirect_uri = 'http://example.com/auth_return'
#      )
#
#  storage = Storage('creds.data')
#  credentials = run_flow(flow, storage, flags)
  json_key = json.load(open('ozaPardy-9bd0550357c8.json'))
  scope = ['https://spreadsheets.google.com/feeds']
  credentials = SignedJwtAssertionCredentials(
    json_key['client_email'],
    json_key['private_key'],
    scope)
  gc = gspread.authorize(credentials)
  print "access_token: %s" % credentials.access_token
  return(gc)

cmd = "OzaPardy cmozafam Jeopardy4us [-h] [-a] [-s] [-d] [-f]"
if len(sys.argv) < 1:
  print (cmd)
  exit()
if len(sys.argv) > 3:
  x = str(sys.argv)
  if '-a' in x:
    print 'Set program in debug mode without Arduino'
    ARDUINO = False
  if '-h' in x:
    print (cmd)
    exit()
  if '-s' in x:
    SINGLE = True
  if '-d' in x:
    DOUBLE = True
  if '-f' in x:
    FINAL = True
else:
  ARDUINO = True  # set this to True if you want to run with arduino/buttons

usbport = '/dev/ttyACM0'
if ARDUINO: ser = serial.Serial(usbport, 9600, timeout=0.10)
ID_TIMER = 2000
ID_TIMER2 = 2001
serDelay = 100
countdownDelay = 1000  # in ms?
mediaDir = 'media/'
#print ser

class ozaPardyBox(object):
  def __init__(self, clue=None, response=None, value=None, 
    isClicked=False, isDailyDouble=False, isAnswered=False,
    MiceAns=0, menAns=0, mediaType=0, mediaFName=''):
    self.clue = clue
    self.response = response
    self.value = value
    self.isClicked = isClicked
    self.isDailyDouble = isDailyDouble
    self.isAnswered = isAnswered
    self.MiceAns = MiceAns
    self.menAns = menAns

    # 0 = Not Media, 1 = Image, 2 = Audio, 3 = Video 
    self.mediaType = mediaType
    self.mediaFName = mediaDir+mediaFName


  def clicked(self):
    self.isClicked = True

  def answered(team, isCorrect):
    if team == 'men':
      self.menAns = isCorrect
      self.isAnswered=True
    elif team == 'Mice':
      self.MiceAns = isCorrect
      self.isAnswered=True
    else:
      print("Team isn't valid: No score changed")


class team(object):
  def __init__(self, name, score=0):
    self.name = name
    self.score = score

  def updateScore(self, points):
    self.score += points


class mainWin(wx.Frame):
  def __init__(self, *args, **kwargs):
    super (mainWin, self).__init__(*args, **kwargs)

    self.tempMsg = ""
    self.serialTimer=wx.Timer(self, ID_TIMER)
    self.Bind(wx.EVT_TIMER, self.timerFunc, self.serialTimer)
    self.serialTimer.Start(serDelay)
    self.serialTimer.Stop()

    self.teams = [team('Mice', 0), team('Men', 0)]
    self.currTeam = 0
    self.lastCorrectTeam = self.currTeam

    self.boxId = [''] * 30
    
    # Make empty gameplay boxes for single jeopardy (sBoxes)
    # Make empty gameplay boxes for double jeopardy (dBoxes)
    # Make empty gameplay boxes for final jeopardy (fBoxes)

    sBoxes = [""] * 6
    for ii in range(30): 
      sBoxes.append(ozaPardyBox())
    dBoxes = [""] * 6
    for ii in range(30): 
      dBoxes.append(ozaPardyBox())
    fBoxes = [""] * 6
    for ii in range(30): 
      fBoxes.append(ozaPardyBox())
    self.boxes = [sBoxes, dBoxes, fBoxes] 
    
    self.FinalBox = ['', ozaPardyBox()]

    self.modes = ['Single', 'Double', 'Final', 'Clue', 'Klok', 
      'Response', 'Daily', 'Blank']
    self.gameMode = 'Single'
    self.currMode = 'Single'
    
    self.wagers = [0, 0]
    
    self.currBox = -1
    self.currClueButton = wx.Button(self)
    self.timeCounter = 15

    [self.MicePanel, self.bPanel, self.menPanel] = self.updateHeader()
#    doc_name = raw_input('What is name of OzaPardy sheet? ',\
#   Sheet must be shared with cmozafam@gmail.com...\nType in Sheetname: ')
    doc_name="OzaPardy"
    [self.stPanel, self.sgPanel] = self.initGameBoxes('Single',doc_name)
    [self.dtPanel, self.dgPanel] = self.initGameBoxes('Double',doc_name)
    self.initFinalBox()

    self.makeDailyDoubles()
    self.dtPanel.Hide()
    self.dgPanel.Hide()
    self.cPanel = self.newClue()
    self.timer = wx.Timer(self, ID_TIMER2)
    self.Bind(wx.EVT_TIMER, self.timerFunc, self.timer)
    self.InitUI()
    self.Center()
    self.ShowFullScreen(False)
    self.Show(True)

  def timerUpdate(self, e):
    self.currClueButton.SetLabel("Time Remaining: " + str(self.timeCounter))

    self.timeCounter -= 1
    if self.timeCounter <= 0:
      self.timer.Stop()
      self.currClueButton.SetLabel("Time's Up!!")

  def readSerial(self, e):
  #   ser = serial.Serial(usbport, 9600)
    self.serialTimer.Stop()
    msg = ser.readline();
    if (msg):
      print "XXXX - Serial Input: " + msg
      self.setCurrTeam(msg.strip())
#DEBUG      print "XXXX - Current Team #: ", self.currTeam
      self.OnClueClickerClicked()
      #self.tempMsg = msg
      #ser.write('W')
      #self.queue.put(msg)
    self.serialTimer.Start()


# This function will restart the Serial port.  This entails flushing the serial
# input buffer, sending an 'R' out on the serial output buffer (to reset the
# Arduino mode), and then starting the serialTimer
# hwStateLetter = [R|W|L] can be any of the following:
#   R: Sets the (R)estartFlag of the HW state to be true
#   W: Tells the HW that a (W)rong answer was given
#   L: Un(L)ocks the HW to enable the clickers
  def restartSerial(self, hwStateLetter):
    self.serialTimer.Stop()
    if ARDUINO:
      ser.flushInput()
      ser.flushOutput()
#DEBUG      print "HW State Letter: ", hwStateLetter
      ser.write(hwStateLetter)
    self.serialTimer.Start()

  def timerFunc(self, e):
    timerId = e.GetId()
    if timerId == ID_TIMER:
#      print "XXXX - Serial Timer Time: ", dt.datetime.now()
#      print "XXXX - Serial Read Timer Event"
      if ARDUINO: self.readSerial(e)
    elif timerId == ID_TIMER2:
      #print "Countdown Timer Time: ", dt.datetime.now()
      #print "Countdown Timer Event"
      self.timerUpdate(e)

  def mode(self, modeType='Single'):
    if modeType in self.modes:
      return self.modes.index(modeType)
    else: return 0
    
  # This routine checkes if all boxes have been clicked & so the game is done.
  def areWeDoneYet(self):
    mNum = self.mode(self.gameMode)
    done = True
    for ii in range(30):
      done = (self.boxes[mNum][ii+6].isClicked and done)
#    print 'gameMode/mNum/done', self.gameMode, mNum, done
    return done

  # gameType variable tells you what round of the game you are in.
  # gameType = 0: Single Jeopardy
  # gameType = 1: Double Jeopardy
  # gameType = 2: Final Jeopardy
  def getJeopardyData(self, gameType=0, doc_name="OzaPardy"):
    #username    = 'cmozafam@gmail.com'
    #passwd      = 'Jeopardy4us'
#    doc_name = raw_input('What is name of OzaPardy sheet? '+
#       Sheet must be shared with cmozafam@gmail.com...\nType in Sheetname: ')
    print "Start getJeopardyData"
    # Connect to Google
#    gd_client = gdata.spreadsheet.service.SpreadsheetsService()
#    gd_client.email = username
#    gd_client.password = passwd
#    gd_client.source = 'ozapardy2015.py'
#    gd_client.ProgrammaticLogin()
#
#    q = gdata.spreadsheet.service.DocumentQuery()
#    q['title'] = doc_name
#    q['title-exact'] = 'true'
#    feed = gd_client.GetSpreadsheetsFeed(query=q)
##    print feed
#    spreadsheet_id = feed.entry[0].id.text.rsplit('/',1)[1]
#    feed = gd_client.GetWorksheetsFeed(spreadsheet_id)
#    worksheet_id = feed.entry[gameType].id.text.rsplit('/',1)[1]
#
#    rows = gd_client.GetListFeed(spreadsheet_id, worksheet_id).entry
#    gc = gspread.login(username, passwd)

#    gc = authorizeOzaPardy()
#    jeopardySpreadsheet = gc.open(doc_name)
#
#    sSht = jeopardySpreadsheet.worksheet("single")
#    dSht = jeopardySpreadsheet.worksheet("double")
#    fSht  = jeopardySpreadsheet.worksheet("final")
#
#    # The following three arrays set the initial data sets
#    singleData = sSht.get_all_values()
#    doubleData = dSht.get_all_values()
#    finalData  = fSht.get_all_values()

    if gameType == 0:
      data = loadtxt('OzaPardy - Single.tsv', dtype='S', delimiter='\t', skiprows=1)
      print('Loaded Single Jeopardy')
    elif gameType == 1:
      data = loadtxt('OzaPardy - Double.tsv', dtype='S', delimiter='\t', skiprows=1)
      print('Loaded Double Jeopardy')
    else:
      print ('Error in getJeopardyData: Invalid gameType')
      return()

    for rowNum, row in enumerate(data):
      for colNum, boxVal in enumerate(row):
        boxNum = int((ceil(rowNum/2.)*6) + (colNum-1))
        if colNum != 0:
          if rowNum == 0:   # Fill in category Names
            self.boxes[gameType][boxNum] = boxVal #row[key].text
          else:         # Fill in Clue/Response boxes
            self.parseOzaPardyBox(self.boxes[gameType][boxNum], boxVal, row[0])

  def getFinalJeopardy(self, doc_name = 'OzaPardy'):
#    username    = 'cmozafam@gmail.com'
#    passwd      = 'Jeopardy4us'
#
#    print "Start getFinalJeopardy"
#    gd_client = gdata.spreadsheet.service.SpreadsheetsService()
#    gd_client.email = username
#    gd_client.password = passwd
#    gd_client.source = 'ozapardy2015.py'
#    gd_client.ProgrammaticLogin()
#
#    q = gdata.spreadsheet.service.DocumentQuery()
#    q['title'] = doc_name
#    q['title-exact'] = 'true'
#    feed = gd_client.GetSpreadsheetsFeed(query=q)
#    spreadsheet_id = feed.entry[0].id.text.rsplit('/',1)[1]
#    feed = gd_client.GetWorksheetsFeed(spreadsheet_id)
#    worksheet_id = feed.entry[2].id.text.rsplit('/',1)[1]
##    print worksheet_id

    finalData  = loadtxt('OzaPardy - Final.tsv', dtype='S', delimiter='\t', skiprows=1)
#    rows = gd_client.GetListFeed(spreadsheet_id, worksheet_id).entry

    self.FinalBox[1].value = 1
    for rowNum, row in enumerate(finalData):
      for colNum, boxVal in enumerate(row):
        boxNum = int(ceil(rowNum/2.) + (colNum-1))
        if rowNum == 0:
          self.FinalBox[0] = boxVal
        if rowNum == 1:
          self.FinalBox[1].clue = self.myWrap(boxVal)
        if rowNum == 2:
          self.FinalBox[1].response = self.myWrap(boxVal)

  # opBox is OzaPardyBox
  # OLD def parseOzaPardyBox(self, opBox, key, gDict):
  # cellData is the first column of the spreadsheet which determines whether
  #     the row is a clue or a response and the point value associated with 
  #     that row.
  def parseOzaPardyBox(self, opBox, boxVal, cellData):
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

  def makeDailyDoubles(self):
    r1 = random.randrange(30)
    r2 = random.randrange(30)
    r3 = random.randrange(30)
    while r2 == r3:
      r3 = random.randrange(30)
    
    self.boxes[0][r1+6].isDailyDouble = True
    self.boxes[1][r2+6].isDailyDouble = True
    self.boxes[1][r3+6].isDailyDouble = True

#DEBUG    print 'DD', r1, r2, r3


  def screenDraw(self, modeType):
#    self.MicePanel.Hide()
#    self.bPanel.Hide()
#    self.menPanel.Hide()
    self.serialTimer.Stop()
    self.stPanel.Hide()
    self.sgPanel.Hide()
    self.dtPanel.Hide()
    self.dgPanel.Hide()
    self.cPanel.Hide()
    self.Show()

    vbox = wx.BoxSizer(wx.VERTICAL)
    hSizer = wx.BoxSizer(wx.HORIZONTAL)

    [self.MicePanel, self.bPanel, self.menPanel] = self.updateHeader()

    hSizer.AddMany([(self.MicePanel, 1, wx.EXPAND),
                    (self.bPanel,  1, wx.EXPAND),
                    (self.menPanel,  1, wx.EXPAND)])

    vbox.Add(hSizer, proportion=6, flag=wx.EXPAND)

    if modeType == 'Single':
      if not self.areWeDoneYet():
        self.stPanel.Show()
        self.sgPanel.Show()
        vbox.Add(self.stPanel, proportion=1, flag=wx.EXPAND)
        vbox.Add(self.sgPanel, proportion=20, flag=wx.EXPAND)
      else:
        self.gameMode = 'Double'
        modeType = 'Double'
        self.cPanel = self.newClue('Double Jeopardy')
        self.cPanel.Show()
        vbox.Add(self.cPanel, proportion=21, flag=wx.EXPAND)
        
    elif modeType == 'Double':
      if not self.areWeDoneYet():
        self.dtPanel.Show()
        self.dgPanel.Show()
        vbox.Add(self.dtPanel, proportion=1, flag=wx.EXPAND)
        vbox.Add(self.dgPanel, proportion=20, flag=wx.EXPAND)
      else:
        self.gameMode = 'Final'
        modeType == 'Final'
        self.cPanel = self.newClue('Final Jeopardy')

        # Print the final jeopardy category, clue, and response to help
        # the moderator.  The moderator is able to use the response 
        # listed to confirm or deny the accuracy of the responses given
        # by each team.
        print('Category: ', self.FinalBox[0])
        #print('Clue: ', self.FinalBox[1].clue)
        print('Response: ', self.FinalBox[1].response)

        self.cPanel.Show()
        vbox.Add(self.cPanel, proportion=21, flag=wx.EXPAND)
    # This elif not is for "Clue", "Response", "Blank", "Klok", "Daily"
    elif not (modeType == 'Single' or modeType == 'Double'):
      self.cPanel.Show()
      vbox.Add(self.cPanel, proportion=21, flag=wx.EXPAND)

    self.SetSizer(vbox)
    self.Layout()
  
  def InitUI(self):
  # The noMenu items are commented out to eliminate showing the File Menu
#noMenu    menubar = wx.MenuBar()  # Create Menubar object
#noMenu    fileMenu = wx.Menu()  # Create Menu opject
#noMenu#    qmi = wx.MenuItem(fileMenu, APP_EXIT, '&Quit\tCtrl+Q')
#noMenu#    qmi.SetBitmap(wx.Bitmap('exit.png'))
#noMenu#    fileMenu.AppendItem(qmi)
#noMenu
#noMenu    fitem = fileMenu.Append(wx.ID_EXIT, '&Quit', 'Quit Jeopardy')
#noMenu    self.Bind(wx.EVT_MENU, self.OnQuit, fitem)
#noMenu    
#noMenu    menubar.Append(fileMenu, '&File')
#noMenu    self.SetMenuBar(menubar)

    self.screenDraw('Single')
    
  def initFinalBox(self):
    mNum = self.mode('Final')
    self.getFinalJeopardy()

  def initGameBoxes(self, modeType, doc_name):
    mNum = self.mode(modeType)
    self.getJeopardyData(mNum, doc_name)
    
    tSizer = wx.GridSizer(1, 6, 2, 2)
    tPanel = wx.Panel(self)
    tPanel.SetSizer(tSizer)

    gSizer = wx.GridSizer(5, 6, 2, 2)
    gPanel = wx.Panel(self)
    gPanel.SetSizer(gSizer)

    for x in range(1,37):
      if x < 7:
        title = wx.Button(tPanel, label=self.boxes[mNum][x-1]) 
        title.SetFont(wx.Font(14, wx.MODERN, wx.NORMAL, wx.BOLD))
        title.SetForegroundColour('white')
        title.SetBackgroundColour('darkblue')
        # if the background color isn't being set properly, check the system 
        # theme settings to ensure a texture isn't isn't overriding the color
        # On ubuntu, choosing Ambiance works
        title.Refresh()
        tSizer.AddMany( [(title, 1, wx.EXPAND)] )
      else:
        self.boxId[x-7] = x-7
        boxButton = wx.Button(gPanel, label=self.boxes[mNum][x-1].value,
          name=str(self.boxId[x-7]))
        boxButton.SetFont(wx.Font(40, wx.MODERN, wx.NORMAL, wx.BOLD))
        boxButton.SetForegroundColour('white')
        boxButton.SetBackgroundColour('blue')
        boxButton.Bind(wx.EVT_BUTTON, self.OnGameButtonClicked)
        gSizer.AddMany( [(boxButton, 1, wx.EXPAND)] )
        
    return [tPanel, gPanel]
  
  def myWrap(self, inStr):
    tmp = textwrap.wrap(inStr, 30)
#    print tmp
    tmp = '\n'.join(tmp) 
    return tmp

  def newClue(self, cString='Text', cType='', cFName=''):
    cPanel = wx.Panel(self)
    
    if cType == 1:
#DEBUG      print "1",cString
#DEBUG      print "2",cType
#DEBUG      print "3",cFName
    
      iSizer = wx.GridSizer(1, 2, 2, 2)
      cPanel.SetSizer(iSizer)
      img = wx.Image(cFName, wx.BITMAP_TYPE_ANY)
      # self.GetSize() returns the width and height of the window
      # wW = window Width, and wH = window Height
      wW, wH = self.GetSize()
      w, h = img.GetSize()
      if w > h:
        NewW = wW * 0.50
        NewH = NewW * h / w
      else:
        NewH = wH * 0.75
        NewW = NewH * w / h
      img = img.Scale(NewW,NewH).ConvertToBitmap()
#DEBUG      print img.GetSize()
      cButton = wx.Button(cPanel, label=cString)
      cButton.SetFont(wx.Font(35, wx.MODERN, wx.NORMAL, wx.BOLD))
      iButton = wx.BitmapButton(cPanel, bitmap=img)
#DEBUG      print iButton.GetSize()
    elif cType == 2:
      # code for audio layout
      print "Audio!"
    elif cType == 3:
      # code for video layout
      print "Video!"
    else:
      cSizer = wx.BoxSizer() 
      cPanel.SetSizer(cSizer)
      cButton = wx.Button(cPanel, label=cString)
      cButton.SetFont(wx.Font(50, wx.MODERN, wx.NORMAL, wx.BOLD))
    #tmpString = self.myWrap(cString)
    #cButton.SetLabel(tmpString)
    cButton.SetForegroundColour('white')
    cButton.SetBackgroundColour('blue')
    cButton.Bind(wx.EVT_BUTTON, self.OnClueButtonClicked)

    if cType == 1:
      iSizer.Add(cButton, 1, wx.EXPAND)
      iSizer.Add(iButton, 1, wx.EXPAND)
    else:
      cSizer.Add(cButton, 1, wx.EXPAND)

    self.currClueButton = cButton
    return cPanel

  
  def OnGameButtonClicked(self, e):
    mNum = self.mode(self.gameMode)
    bName = int(e.GetEventObject().GetName())
    
    self.timeCounter = 15
    e.GetEventObject().SetLabel('')
    self.currBox = bName+6

#DEBUG    print ('bName:' , bName)
    tmpBox = self.boxes[mNum][bName+6]
    if tmpBox.isClicked == False:
      tmpBox.clicked()
      e.GetEventObject().Disable()
      self.cPanel=self.newClue(tmpBox.clue, tmpBox.mediaType, tmpBox.mediaFName)
      if tmpBox.isDailyDouble:
        print 'Daily Double Selected', self.currMode
        self.currMode = 'Clue'
        self.cPanel = self.newClue('Daily Double')
        self.screenDraw('Clue')
      else: 
        self.screenDraw('Clue')
        #ser.write('L')  # Unlock Arduino controller
#DEBUG        print 'XXXX - Serial Write: L'
        #self.serialTimer.Start(serDelay)
        #self.serialTimer.Start()
        self.restartSerial('L')
      #print "Clue: ", tmpBox.clue
      print "Response: ", tmpBox.response, "\n"
    
  def OnClueButtonClicked(self, e):
    tic = dt.datetime.now()
    mNum = self.mode(self.gameMode)
    #clueText = self.boxes[mNum][self.currBox].clue
    tmpBox = self.boxes[mNum][self.currBox]
    clueText = tmpBox.clue

    self.serialTimer.Stop()
    if self.currMode == 'Response':
      self.currMode = self.gameMode
      self.screenDraw(self.currMode)
    else:
      btnLabel = e.GetEventObject().GetLabel()
      if btnLabel == clueText:
        if self.currMode != 'Daily':
          self.currMode = 'Blank'
        self.screenDraw('Blank')
        #self.currMode = 'Klok'
        #self.screenDraw('Klok')
        # self.timer.Start(countdownDelay)
        # self.currClueButton = e.GetEventObject()
        e.GetEventObject().SetLabel("")
#DEBUG        print "Going blank"
        #e.GetEventObject().SetLabel("Time Remaining: " + str(self.timeCounter))
      elif btnLabel == 'Daily Double':
        self.currMode = 'Daily'
        self.timer.Stop()
        self.timeCounter = 15
        self.cPanel = self.newClue(tmpBox.clue, tmpBox.mediaType,
                                   tmpBox.mediaFName)
        self.screenDraw('Clue')
#        e.GetEventObject().SetLabel(clueText)
      elif btnLabel == '':
        self.screenDraw('Clue')
        if self.currMode != 'Daily':
          self.currMode = 'Clue'
          self.timer.Stop()
          self.restartSerial('R') # Restart the Serial Port
#DEBUG          print "restarting Serial Port 'R'"
          time.sleep(.05)
          self.restartSerial('L') # Unlock the clickers; enable clickers
#DEBUG          print "Unlocking clickers"
#          self.serialTimer.Start()
          if self.timeCounter < 10:
            self.timeCounter = 10
        e.GetEventObject().SetLabel(clueText)
#DEBUG        print "Showing Clue after Blank"
      elif btnLabel == 'Double Jeopardy':
        self.currMode = self.gameMode
        self.screenDraw(self.currMode)
      elif btnLabel == 'Final Jeopardy':
        self.screenDraw('FinalCategory')
        e.GetEventObject().SetLabel(self.FinalBox[0])
      elif btnLabel == self.FinalBox[0]:
        self.screenDraw('FinalClue')
        e.GetEventObject().SetLabel(self.FinalBox[1].clue)
      elif btnLabel == self.FinalBox[1].clue:
        self.screenDraw('FinalResponse')
        e.GetEventObject().SetLabel(self.FinalBox[1].response)
      else:
      # This should only happen when the screen is displaying the timer
      # countdown, and then the mouse clicks the cPanel. The timer 
      # countdown should only be displayed if a clicker was clicked or 
      # after the clue was displayed for the Daily Double
        # self.currMode = 'Clue'
        # self.screenDraw('Clue')
        # self.timer.Stop()
        # if self.timeCounter < 10:
        #   self.timeCounter = 10
        # e.GetEventObject().SetLabel(clueText)
        print "Host tried to click the timer.."

    self.Layout()
    toc = dt.datetime.now()
#    print "button: ", toc-tic

  # This function is called when the clue button is displayed and the clicker
  # is clicked
  def OnClueClickerClicked(self):
    tic = dt.datetime.now()
    mNum = self.mode(self.gameMode)
    clueText = self.boxes[mNum][self.currBox].clue
    self.serialTimer.Stop()
#DEBUG    print "XXXX - In On Clue Clicker"
    if self.currMode == 'Response':
      # This code should never happen
      print "This should never happen:(OnClueClickerClicked) Clicker"+\
        "should never do anything if the response is visible" 
      self.currMode = self.gameMode
      self.screenDraw(self.currMode)
    else:
      btnLabel = self.currClueButton.GetLabel()
#DEBUG      print btnLabel
      if btnLabel == clueText:
        # If label == Clue, change state to Klok
        self.currMode = 'Klok'
        self.screenDraw('Klok')
        self.timer.Start(countdownDelay)
        self.currClueButton.SetLabel("Time Remaining: "+ str(self.timeCounter))
#      elif btnLabel == 'Daily Double':
#       # If label == Daily Double, set state to Daily Double
#        self.currMode = 'Daily'
#        self.screenDraw('Daily')
#        self.timer.Stop()
#        self.timeCounter = 15
#        self.currClueButton.SetLabel(clueText)
      else:
        print "clicker was clicked w/ cPanel was blank, daily double, or timer"
#        self.currMode = 'Clue'
#        self.screenDraw('Clue')
#        self.timer.Stop()
#        if self.timeCounter < 10:
#          self.timeCounter = 10
#        self.currClueButton.SetLabel(clueText)
    self.Layout()
    toc = dt.datetime.now()
#    print "Clicker: ", toc-tic

  def OnOzaPardyButtonClicked(self, e):
    mNum = self.mode(self.gameMode)
    self.boxes[mNum][self.currBox].isAnswered = True
    self.timer.Stop()
    self.serialTimer.Stop()
    self.currMode = 'Response'
    self.cPanel = self.newClue(self.boxes[mNum][self.currBox].response)
    self.screenDraw('Response')
    
  def OnCorrectButtonClicked(self, e):
    mNum = self.mode(self.gameMode)
    self.boxes[mNum][self.currBox].isAnswered = True
    self.timer.Stop()
    self.serialTimer.Stop()
    ser.write('C')
    points = int(self.boxes[mNum][self.currBox].value)
#DEBUG    print "XXXX - Current team: ", self.currTeam, points
    self.teams[self.currTeam].updateScore(points)
    self.lastCorrectTeam = self.currTeam
    self.currMode = 'Response'
    self.cPanel = self.newClue(self.boxes[mNum][self.currBox].response)
    self.screenDraw('Response')
    #FIGURE OUT SCORING HERE

  def OnWrongButtonClicked(self, e):
    mNum = self.mode(self.gameMode)
    self.boxes[mNum][self.currBox].isAnswered = True
    self.timer.Stop()
    self.serialTimer.Stop()
    #ser.write('W')
    points = int(self.boxes[mNum][self.currBox].value)
#DEBUG    print "XXXX - Current team: ", self.currTeam, -1*points
    self.teams[self.currTeam].updateScore(-1*points)
    self.currMode = 'Clue'


    #print ('currBox: ', self.currBox)
    tmpBox = self.boxes[mNum][self.currBox]
    self.cPanel = self.newClue(tmpBox.clue, tmpBox.mediaType,
                               tmpBox.mediaFName)
#      self.cPanel = self.newClue(self.boxes[mNum][self.currBox].clue)
    self.screenDraw('Clue')
    #self.serialTimer.Start(serDelay)
    #self.serialTimer.Start()
    self.restartSerial('W')

  def OnQuit(self, e):
    self.Close()
    
  def updateHeader(self):
    smallNormal = wx.Font(15, wx.MODERN, wx.NORMAL, wx.BOLD)
    bigNormal = wx.Font(30, wx.MODERN, wx.NORMAL, wx.BOLD)
    biggerNormal = wx.Font(50, wx.MODERN, wx.NORMAL, wx.BOLD)
    smallItalic = wx.Font(15, wx.MODERN, wx.ITALIC, wx.BOLD)
    bigItalic = wx.Font(30, wx.MODERN, wx.ITALIC, wx.BOLD)
    biggerItalic = wx.Font(50, wx.MODERN, wx.ITALIC, wx.BOLD)

    MicePanel = wx.Panel(self)
    MiceTitle = wx.StaticBox(MicePanel, label=self.teams[0].name,
      pos=(5,5), size=(550,210))
    MiceTitle.SetFont(bigItalic)

    MiceScoreDisp = wx.StaticText(MicePanel, 1, pos=(20,80))
    MiceScoreDisp.SetLabel('$' + str(self.teams[0].score))
    MiceScoreDisp.SetFont(bigNormal)
    MiceScoreDisp.SetForegroundColour('blue')
    MiceWagerLabel = wx.StaticText(MicePanel, 1, pos=(320,60))
    MiceWagerLabel.SetLabel('Wager')
    MiceWagerLabel.SetFont(smallNormal)
    MiceWager = wx.TextCtrl(MicePanel, 1, pos=(220,90), size=(200,50))
    MiceWager.Bind(wx.EVT_TEXT, self.updateMiceWager)
    MiceWager.SetFont(bigNormal)
    
    bPanel = wx.Panel(self)
    if self.currMode != 'Klok':
      midButton = wx.Button(bPanel, pos=(5,25), size=(550,70), label='OzaPardy')
      midButton.SetFont(bigNormal)
      midButton.SetForegroundColour('darkblue')
      midButton.Bind(wx.EVT_BUTTON, self.OnOzaPardyButtonClicked)
    if self.currMode == 'Klok' or self.currMode == 'Daily':
      corButton = wx.Button(bPanel, pos=(5,104), size=(550,50), label='Correct')
      wrgButton = wx.Button(bPanel, pos=(5,163), size=(550,50), label='Wrong')
      corButton.SetFont(smallNormal)
      wrgButton.SetFont(smallNormal)
      corButton.SetForegroundColour('darkgreen')
      wrgButton.SetForegroundColour('red')
      corButton.Bind(wx.EVT_BUTTON, self.OnCorrectButtonClicked)
      wrgButton.Bind(wx.EVT_BUTTON, self.OnWrongButtonClicked)

    menPanel = wx.Panel(self)
    menTitle = wx.StaticBox(menPanel, label=self.teams[1].name,
      pos=(5,5), size=(550,210))
    menTitle.SetFont(bigItalic)

    # Handle coloring of the Men/Mice Title bars based on who clicked 
    # and/or who owns the board
    if (self.currMode == 'Klok' and self.currTeam == 0) or (self.currMode != 'Klok' and self.lastCorrectTeam == 0):
      MiceTitle.SetForegroundColour('darkblue')
      menTitle.SetForegroundColour('darkgrey')
      menTitle.SetFont(bigNormal)
    #else:
    #  MiceTitle.SetForegroundColour('darkgrey')
    if (self.currMode == 'Klok' and self.currTeam == 1) or (self.currMode != 'Klok' and self.lastCorrectTeam == 1):
      menTitle.SetForegroundColour('darkblue')
      MiceTitle.SetForegroundColour('darkgrey')
      MiceTitle.SetFont(bigNormal)
    #else:
    #  menTitle.SetForegroundColour('darkgrey')
    menScoreDisp = wx.StaticText(menPanel, 1, pos=(20,80))
    menScoreDisp.SetLabel('$' + str(self.teams[1].score))
    menScoreDisp.SetFont(bigNormal)
    menScoreDisp.SetForegroundColour('blue')
    menWagerLabel = wx.StaticText(menPanel, 1, pos=(320,60))
    menWagerLabel.SetLabel('Wager')
    menWagerLabel.SetFont(smallNormal)
    menWager = wx.TextCtrl(menPanel, 1, pos=(220,90), size=(200,50))
    menWager.Bind(wx.EVT_TEXT, self.updateMenWager)
    menWager.SetFont(bigNormal)

    return [MicePanel, bPanel, menPanel]

  def updateMiceWager(self, e):
    wager = e.GetEventObject().GetValue()
    mNum = self.mode(self.gameMode)
    self.currTeam = 0
    self.wagers[self.currTeam] = wager
    self.boxes[mNum][self.currBox].value = wager

  def updateMenWager(self, e):
    wager = e.GetEventObject().GetValue()
    mNum = self.mode(self.gameMode)
    self.currTeam = 1
    self.wagers[self.currTeam] = wager
    self.boxes[mNum][self.currBox].value = wager

  def setCurrTeam(self, serRead):
#DEBUG    print 'XXXX - Serial Read:', serRead, serRead == 'Mice'

    if serRead == 'Mice':
      self.currTeam = 0
#DEBUG      print "currTeam now Mice", self.currTeam
    else:
      self.currTeam = 1
#DEBUG      print "currTeam now Men", self.currTeam

def main():
  app = wx.App()
#  mainWindow= wx.Frame(None, -1, 'OzaPardy', style =  wx.MAXIMIZE_BOX |
#    wx.RESIZE_BORDER | wx.CAPTION | wx.CLOSE_BOX)
  #mainWin(None)
  print("Authorization access required")
  mainWin(None, title='OzaPardy', size=(1600, 900),
    style=wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | wx.CAPTION | wx.CLOSE_BOX,
    name='Noza')
  app.MainLoop()

if __name__ == '__main__':
  main()

