from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown 


# Builder.load_file('graphics/clue.kv')

class Switcher(ScreenManager):
    pass

kv = Builder.load_file('graphics/brozapardy.kv')

class SetupDrop(DropDown):
    def __init__(self, **kw):
        super(SetupDrop, self).__init__(**kw)
        self.ddn = DropDown()
        self.ddn.bind(on_press=self.on_select)

class BrOzaPardy(App):
    def build(self):
        return kv
        
    def setup(self):
        print('In the Setup routine********')
        




if __name__ == '__main__':
    BrOzaPardy().run()

