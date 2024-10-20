from kivy.uix.screenmanager import ScreenManager, SwapTransition
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, StringProperty
from kivy.lang import Builder


from kivymd.app import MDApp
from kivymd.uix.screen import Screen 
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp


from utils.database import DatabaseHandler
from utils.helpers import is_valid, BaseScreen, jahrgang_valid
from utils.popup import WarningPopup

import sqlite3

class SchuleApp(MDApp):
    def build(self):
        self.db_handler = DatabaseHandler("schule.db")

        kv_files = [
            'kv/home.kv',
            'kv/klassen.kv',
            'kv/schueler.kv',
            'kv/beurteilung.kv'
        ]

        for kv_file in kv_files:
            Builder.load_file(kv_file)

        sm = WindowManager(transition=SwapTransition())
        sm.add_widget(HomeScreen(name='home', db_handler=self.db_handler))
        sm.add_widget(KlassenScreen(name='klassen', db_handler=self.db_handler))
        sm.add_widget(SchuelerScreen(name='schueler', db_handler=self.db_handler))
        sm.add_widget(BeurteilungsScreen(name='beurteilung', db_handler=self.db_handler))
        return sm

    def on_stop(self):
        self.db_handler.db_schliessen()

class HomeScreen(BaseScreen):
    target_screen = 'beurteilung'# Screen when a class is pressed
    title = ObjectProperty(None)

    def open_dropdown(self, instance):
        jahrgaenge = self.db_handler.jahrgaenge_auslesen()
        items = []  # Define your dropdown items here
        for jahrgang in jahrgaenge:
            items.append(jahrgang[0])
        items = sorted(items)
        screen_instance = self.manager.get_screen('klassen')
        self.on_dropdown( instance, items, self.title, screen_instance)
        self.display_classes()
        
    


class KlassenScreen(BaseScreen):
    input_klasse = ObjectProperty(None)
    target_screen = 'schueler'
    seleted_text = StringProperty("")

    def add_class(self):
        klasse = self.input_klasse.text
        jahrgang = self.selected_text
        if is_valid(klasse):
            try:
                self.db_handler.klasse_hinzufuegen(klasse, jahrgang)
                self.display_classes()
                self.input_klasse.text = ""
                print(f"Selected Jahrgang: {self.selected_text}")
            except sqlite3.IntegrityError:
                popup = WarningPopup(message="Klasse bereits vorhanden")
                popup.open()
        else: 
            popup = WarningPopup(message="Ungültige Klasse")
            popup.open()

    def add_year(self):
        jahrgang = self.ids.input_jahrgang.text
        if jahrgang_valid(jahrgang):
            self.db_handler.jahrgang_hinzufuegen(jahrgang)
            self.ids.input_jahrgang.text = ""
        else:
            popup = WarningPopup(message="Ungültiger Jahrgang")
            popup.open()

class SchuelerScreen(Screen):
    pressed_class = StringProperty("")
    input_vorname = ObjectProperty(None)
    input_nachname = ObjectProperty(None)

    def __init__(self, db_handler, **kwargs):
        self.db_handler = db_handler
        super(SchuelerScreen, self).__init__(**kwargs)

    def add_student(self):
        klasse = self.pressed_class
        vorname = self.input_vorname.text.title()
        nachname = self.input_nachname.text.title()

        if vorname and nachname:
            try:
                self.db_handler.schueler_hinzufuegen(vorname, nachname, klasse)
                self.input_vorname.text = ""
                self.input_nachname.text = ""
                self.display_student(klasse)

            except sqlite3.IntegrityError:
                popup = WarningPopup(message="Name bereit vorhanden")
                popup.open()

        else:
            popup = WarningPopup(message="Vorname UND Nachname")
            popup.open()
        
    def display_student(self, klasse):
        alle_schueler = self.db_handler.schueler_auslesen(klasse)
        alle_schueler_sorted = sorted(alle_schueler, key=lambda x : x[1])
        self.ids.list_container.clear_widgets()
        for schueler in alle_schueler_sorted:
            label = Label(text=f"> {schueler[1]} {schueler[0]}")
            self.ids.list_container.add_widget(label)
            print(schueler[1],schueler[0])

    def on_enter(self):
        self.ids.klasse_text.text= f"Schüler hinzufügen {self.pressed_class}"
        self.display_student(self.pressed_class)

class BeurteilungsScreen(Screen):
    pressed_class = StringProperty("")
    def __init__(self, db_handler, **kwargs):
        self.db_handler = db_handler
        super(BeurteilungsScreen, self).__init__(**kwargs)

    def on_enter(self):
        self.ids.kl.text= f"Schüler hinzufügen {self.pressed_class}"
        alle_schueler=self.db_handler.schueler_auslesen(self.pressed_class)
        alle_schueler_sorted = sorted(alle_schueler, key=lambda x : x[1])
        header=[("Vorname", dp(30)),("Nachname", dp(30))]
        table = MDDataTable(
            size_hint=(0.9, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            column_data=header,
            row_data=alle_schueler_sorted
            
        )

        self.add_widget(table)


class WindowManager(ScreenManager):
    pass



if __name__ == '__main__':
    SchuleApp().run()