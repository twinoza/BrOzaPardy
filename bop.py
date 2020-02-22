# This App needs the following files to operate:
# bop.py
#
# graphics/bop.kv
# graphics/templates.kv
# graphics/scoreboard.kv
# graphics/cluesol.kv
# graphics/menu.kv


import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.factory import Factory
# from kivy.core.window import Window
from kivy.config import Config

from kivy.properties import ObjectProperty, StringProperty
Config.set('graphics', 'fullscreen', 'real')
# Config.set('graphics', 'height', '100%')
# Config.set('graphics', 'width', '100%')


kivy.require('1.9.0')

# load all thew graphics files
Builder.load_file('graphics/bop.kv')
Builder.load_file('graphics/templates.kv')
Builder.load_file('graphics/scoreboard.kv')
Builder.load_file('graphics/cluesol.kv')
Builder.load_file('graphics/menu.kv')

class BkLabel:
    pass

class HoverLabel:
    pass

class Scrbd(BoxLayout):
    vtm1 = ObjectProperty('Home')
    vscore1 = ObjectProperty(None)
    vtm2 = ObjectProperty()
    vscore2 = ObjectProperty()
    def __init__(self, **kwargs):
        # self.register_event_type('on_newScore')
        super(Scrbd, self).__init__(**kwargs)
        # self.score1.text = '000'

    def changeText(self, team, newVal):
        # print('In ScoreMod --> vnewScore = '+ScoreMod().ids.vnewScore.text + '    vScore-->'+Factory.Scrbd().ids.score1.text)
        # newVal = ScoreMod().newScore
        if team == 'team1':
            # self.score1.bind(text=newVal.setter('text'))
            self.vscore1.text = newVal.text
            # self.score1 = '555'
        else:
            self.vscore2.text = newVal
        print('End of ScoreMod --> newScore = '+self.vtm1.text + '    Score-->'+ self.vscore1.text) # Factory.Scrbd.score1)

class ScoreMod(Popup):
    vnewScore = ObjectProperty()

    def __init__(self, **kwargs):
        # self.register_event_type('on_newScore')
        super(ScoreMod, self).__init__(**kwargs)
        # self.vnewScore.text = '000'

    def on_newScore(self, team, newVal):
        Factory.Scrbd().changeText(team, newVal)


# Make an app by deriving from the kivy provided app class
class BrOzaPardy(App):
    size_hint = 1,1
    # override the build method and return the root widget of this App
    def build(self):
        return MainWin()

    
    def setup(self):
        # this method is only called when the "BrOzaPardy" button at the top center of scoreboard.kv is clicked.    When this button is pressed, the menu popup is displayed
        print('********Clicked on BrOzaPardy Button for Setup')
        pup = Factory.MenuPopup()
        pup.title = 'Menu'
        pup.text = "This is the new text"
        pup.open()
        
    def initApp(self, gmType):
        print('********Initialize the App '+gmType)
        if gmType == "Init":
            pass
        if gmType == "Single":
            pass
        if gmType == "Double":
            pass
        if gmType == "Final":
            pass
        if gmType == "ScoreMod":
            pass
        
        # todo: get teamnames and set names on ClueSolPopup
        # todo: self.tm1Name = Factory.Scrbd().ids.tmName1.text
        # todo: self.tm2Name = Factory.Scrbd().ids.tmName2.text
        # todo: print('Team1 name is : '+tm1)
        
        # todo: set labels for all categories

    def tm1_clickedIn(self):
        print ("Team1 was selected")

class MainWin(Widget):
    def gridBtnClicked(self, btnClicked):
        print('*******************Starting up show_popup')
        pup = Factory.ClueSolPopup()     # get the Clue Popup
        scrbd = Factory.Scrbd()                # get the scorebd
        category = btnClicked.parent.catLabel.text    # get current category
        pup.content.children[1].text = scrbd.ids.tmName1.text    #set tm1 name
        pup.content.children[0].text = scrbd.ids.tmName2.text    #set tm2 name
        title = category + ' - for: ' + btnClicked.text
        print(title)
        pup.title = title
        pup.text = "This is the new text"    # dummy placeholder
        pup.open()

if __name__ == '__main__':
    BrOzaPardy().run()