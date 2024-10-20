import re
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown

class BaseScreen(Screen):
    display_klassen = ObjectProperty(None)

    def __init__(self, db_handler, **kwargs):
        self.db_handler = db_handler
        super(BaseScreen, self).__init__(**kwargs)

    def display_classes(self):
        klassen = self.db_handler.klassen_auslesen()
        klassen.sort()
        self.display_klassen.clear_widgets()
        for klasse in klassen:
            btn = Button(text=klasse[0], size_hint_x=0.7,size_hint=(None,None),height=30,width=200, pos_hint={'center_x':0.5})
            btn.bind(on_release=self.on_klasse_button_press)
            self.display_klassen.add_widget(btn)

    def on_klasse_button_press(self, instance):
        schueler_screen = self.manager.get_screen(self.target_screen)
        schueler_screen.pressed_class = instance.text
        self.manager.current = self.target_screen
        

    def on_enter(self):
        self.display_classes()

    def on_dropdown(self,button_instance, items, title, screen_instance):
        dropdown = DropDown(auto_dismiss=False)
        for item in items:
            btn = Button(text=item, size_hint_y=None, height=50)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)
        dropdown.bind(on_select=lambda instance, x: self.on_item_selected(button_instance, x, title, screen_instance))
        dropdown.open(button_instance)

    def on_item_selected(self,button_instance, selected_text, title, screen_instance):
        print(f"Selected item: {selected_text}")
        button_instance.text = selected_text
        title.text = selected_text
        screen_instance.selected_text = selected_text 
        # Update the selected_text property of the screen instance



def is_valid(klasse):
    pattern=r"^[1-4][a-f]?$"
    return re.match(pattern, klasse) is not None



def jahrgang_valid(jahrgang):
    pattern = r"^\d{4}/\d{4}$"
    return re.match(pattern, jahrgang) is not None