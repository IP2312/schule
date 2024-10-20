from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty

class WarningPopup(Popup):
    def __init__(self,message, **kwargs):
        super(WarningPopup, self).__init__(**kwargs)
        self.message = message
        
        # Create the main layout
        content = FloatLayout()
        
        # Create the close button
        close_button = Button(text='X', size_hint=(None, None), size=(40, 40),
                              pos_hint={'right': 1, 'top': 1})
        close_button.bind(on_release=self.dismiss)
        
        # Add the close button to the main content
        content.add_widget(close_button)
        
        # Create a vertical layout for the label
        label_layout = BoxLayout(orientation='vertical', size_hint=(1, None), height=50,
                                 pos_hint={'center_x': 0.5, 'center_y': 0.5})
        
        # Add the label to the label layout
        label_layout.add_widget(Label(text=self.message, font_size=25))
        
        # Add the label layout to the main content
        content.add_widget(label_layout)
        
        # Initialize the Popup without a title
        self.title = ''  # Remove the title
        self.separator_height = 0  # Remove the separator (title bar)
        self.content = content
        self.size_hint = (None, None)
        self.size = (400, 200)
        self.auto_dismiss = False  # Ensure the popup doesn't close automatically
        