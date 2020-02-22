from kivy.app import App
from kivy.uix.dropdown import DropDown
from kivy.uix.boxlayout import BoxLayout

class CustomDropDown(BoxLayout):
  pass

class MenuApp(App):
  def build(self):
    return CustomDropDown()
if __name__=='__main__':
  MenuApp().run()