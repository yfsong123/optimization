"""
Config Example
==============

This file contains a simple example of how the use the Kivy settings classes in
a real app. It allows the user to change the caption and font_size of the label
and stores these changes.

When the user next runs the programs, their changes are restored.

"""

from kivy.app          import App
from kivy.uix.settings import SettingsWithTabbedPanel
from kivy.logger       import Logger
from kivy.lang         import Builder
from kivy.uix.button   import Button
from kivy.core.text    import LabelBase
from kivy.properties   import StringProperty
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, NoTransition
import os
import webbrowser
import numpy as np
# The website of the font is in the below:
# https://www.fontsquirrel.com/
# the tutorial video is
# https://www.youtube.com/watch?v=Y5piQF0Rh-M
LabelBase.register(name="rubiklight",
             fn_regular= "Rubik-Light.ttf"      )

class FirstPage(Screen):
    def test(self):
        pass

class MainPage(Screen):
    def test(self):
        pass
    

    

class Connected(Screen):
    def connected(self):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'mainpage'
        

    def disconnect(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
        self.manager.get_screen('login').resetForm()

class Forgot(Screen):
    def reset_password(self):
        return
    def back_to_login(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
        self.manager.get_screen('login').resetForm()

class ExampleScreenNA(Screen):
    def go_na(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'examplescreenna'
    def go_emea(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'examplescreenemea'
    def go_apac(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'examplescreenapac'  
    def go_web(self):
        webbrowser.open("http://kivy.org/")
    pass

class ExampleScreenEMEA(Screen):
    def go_na(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'examplescreenna'
    def go_emea(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'examplescreenemea'
    def go_apac(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'examplescreenapac'  
    pass
class ExampleScreenAPAC(Screen):
    def go_na(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'examplescreenna'
    def go_emea(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'examplescreenemea'
    def go_apac(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'examplescreenapac'  
    pass


    
class Login(Screen):
    def do_login(self, loginText, passwordText):
        app = App.get_running_app()

        app.username = loginText
        app.password = passwordText

        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'connected'

        app.config.read(app.get_application_config())
        app.config.write()
    
    def forgot(self):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'forgot'
        
    def resetForm(self):
        self.ids['login'].text = ""
        self.ids['password'].text = ""

class LoginApp(App):
    username = StringProperty(None)
    password = StringProperty(None)

    def build(self):
        self.icon = './figures/myicon.jpg'
        manager = ScreenManager()

        manager.add_widget(Login(name='login'))
        manager.add_widget(Connected(name='connected'))
        manager.add_widget(Forgot(name='forgot'))
        manager.add_widget(MainPage(name='mainpage'))
        #manager.add_widget(CustomDropDown(name='customdropdown'))
        manager.add_widget(FirstPage(name='firstpage'))
        manager.add_widget(ExampleScreenNA(name='examplescreenna'))
        manager.add_widget(ExampleScreenEMEA(name='examplescreenemea'))
        manager.add_widget(ExampleScreenAPAC(name='examplescreenapac'))
        
        return manager

    def get_application_config(self):
        if(not self.username):
            return super(LoginApp, self).get_application_config()

        conf_directory = self.user_data_dir + '/' + self.username

        if(not os.path.exists(conf_directory)):
            os.makedirs(conf_directory)

        return super(LoginApp, self).get_application_config(
            '%s/config.cfg' % (conf_directory)
        )
        

# We first define our GUI
kv = '''
BoxLayout:
    orientation: 'vertical'
    Button:
        text: 'Configure app (or press F1)'
        on_release: app.open_settings()
    Button:
        text: 'Run Optimizer'
        size_hint: 0.5, 0.2
        
    Button:
        text: 'Plot'
        size_hint: 0.5, 0.2
    Label:
        id: label
        text: 'Hello Yunfei'
'''

# This JSON defines entries we want to appear in our App configuration screen
json = '''
[
    {
        "type": "string",
        "title": "Label caption",
        "desc": "Choose the text that appears in the label， YunFei Song",
        "section": "My Label",
        "key": "text"
    },
    {
        "type": "numeric",
        "title": "Label font size",
        "desc": "Choose the font size the label, Song",
        "section": "My Label",
        "key": "font_size"
    },
    {
        "type": "string",
        "title": "Region",
        "desc": "Set the region, e.g., NA, EMEA, APAC",
        "section": "My Label",
        "key": "region"
    },
    {
        "type": "numeric",
        "title": "Investment Capital",
        "desc": "Set the capital maximum allocation on this region",
        "section": "My Label",
        "key": "capital"
    },
    {
        "type": "numeric",
        "title": "Maximum Investments",
        "desc": "Set the maximum of the investments",
        "section": "My Label",
        "key": "max_name"
    },
    {
        "type": "numeric",
        "title": "Test ",
        "desc": "Set the maximum of the investments",
        "section": "Your Label",
        "key": "max_name_hi"
    }
    
]
'''


class PortfolioOptimizer(App):
    def build(self):
        """
        Build and return the root widget.
        """
        # The line below is optional. You could leave it out or use one of the
        # standard options, such as SettingsWithSidebar, SettingsWithSpinner
        # etc.
        self.settings_cls = MySettingsWithTabbedPanel
        self.icon = 'myicon.jpg'
        
        # We apply the saved configuration settings or the defaults
        root = Builder.load_string(kv)
        label = root.ids.label
        label.text = self.config.get('My Label', 'text')
        label.font_size = float(self.config.get('My Label', 'font_size'))
        label.color = [1,1,1,1]
        button = Button(text='YFSong My first button')
        root.add_widget(button)
        return root

    def build_config(self, config):
        """
        Set the default values for the configs sections.
        """
        config.setdefaults('My Label', {'text': 'Hello', 'font_size': 20, 'region': 'NA', 'capital': 1000000.0,
                                        'max_name': 20})
        config.setdefaults('Your Label', {'max_name_hi': 50})

    def build_settings(self, settings):
        """
        Add our custom section to the default configuration object.
        """
        # We use the string defined above for our JSON, but it could also be
        # loaded from a file as follows:
        #     settings.add_json_panel('My Label', self.config, 'settings.json')
        settings.add_json_panel('My Label', self.config, data=json)

    def on_config_change(self, config, section, key, value):
        """
        Respond to changes in the configuration.
        """
        Logger.info("main.py: App.on_config_change: {0}, {1}, {2}, {3}".format(
            config, section, key, value))

        if section == "My Label":
            if key == "text":
                self.root.ids.label.text = value
            elif key == 'font_size':
                self.root.ids.label.font_size = float(value)

    def close_settings(self, settings=None):
        """
        The settings panel has been closed.
        """
        Logger.info("main.py: App.close_settings: {0}".format(settings))
        super(PortfolioOptimizer, self).close_settings(settings)


class MySettingsWithTabbedPanel(SettingsWithTabbedPanel):
    """
    It is not usually necessary to create subclass of a settings panel. There
    are many built-in types that you can use out of the box
    (SettingsWithSidebar, SettingsWithSpinner etc.).

    You would only want to create a Settings subclass like this if you want to
    change the behavior or appearance of an existing Settings class.
    """
    def on_close(self):
        Logger.info("main.py: MySettingsWithTabbedPanel.on_close")

    def on_config_change(self, config, section, key, value):
        Logger.info(
            "main.py: MySettingsWithTabbedPanel.on_config_change: "
            "{0}, {1}, {2}, {3}".format(config, section, key, value))


#PortfolioOptimizer().run()

LoginApp().run()