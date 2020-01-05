# This App needs the following files to operate:
# bop.py

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
# from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.factory import Factory

kivy.require('1.9.0')

Builder.load_file('graphics/bop.kv')
Builder.load_file('graphics/templates.kv')
Builder.load_file('graphics/scoreboard.kv')
Builder.load_file('graphics/cluesol.kv')
Builder.load_file('graphics/menu.kv')

# Make an app by deriving from the kivy provided app class


class BrOzaPardy(App):
  # override the build method and return the root widget of this App
  def build(self):
    # self.menuPopup = MenuPopup()
    self.mainWin = MainWin()
    # self.menuWin = MenuPopup()
    return self.mainWin

  def setup(self):
    print('********Clicked on BrOzaPardy Button for Setup')
    pup = Factory.MenuPopup()
    pup.title = 'Menu'
    pup.text = "This is the new text"
    pup.open()

  def initApp(self, clickedBtn):
    print('********Initialize the App')
    # set labels for all categories
    # clickedBtn.parent.close()

# class MenuPopup(Popup):
#   pass

class MainWin(Widget):
  # popup = object()

  # def __init__(self, **kwargs):
  #   super(MyManager, self).__init__(**kwargs)
  #   self.popup = ClueSolPopup()
  #   self.bind(current=self.popup.changeText)

  def gridBtnClicked(self,answer_txt):
    print('*******************Starting up show_popup')
    pup = Factory.ClueSolPopup()
    pupTitle = pup.title
    title = pupTitle + ' - value: ' + answer_txt
    print(title) #.P().ids.solution.text)
    Factory.ClueSolPopup.title = title
    Factory.ClueSolPopup.text = "This is the new text"
    Factory.ClueSolPopup().open() 

if __name__ == '__main__':
  BrOzaPardy().run()