import sqlite3

class DatabaseHandler:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS jahrgaenge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                jahrgang TEXT UNIQUE NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS klassen (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                klasse TEXT UNIQUE NOT NULL, 
                jahrgang_id INTEGER,
                FOREIGN KEY (jahrgang_id) REFERENCES jahrgaenge(id) ON DELETE CASCADE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS schueler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Vorname TEXT NOT NULL,
                Nachname TEXT NOT NULL,
                klasse_id INTEGER,
                FOREIGN KEY (klasse_id) REFERENCES klassen(id) ON DELETE SET NULL,
                UNIQUE(Vorname,Nachname)
            )
        ''')
        self.conn.commit()


    def jahrgang_hinzufuegen(self, jahrgang):
        self.cursor.execute("INSERT INTO jahrgaenge (jahrgang) VALUES (?)", (jahrgang,))
        self.conn.commit()

    def klasse_hinzufuegen(self, klasse, jahrgang):
        self.cursor.execute(
            "INSERT INTO klassen (klasse, jahrgang_id) VALUES (?,(SELECT id FROM jahrgaenge WHERE jahrgang = ?))",
            (klasse, jahrgang,)
            )
        self.conn.commit()
    
    def schueler_hinzufuegen(self, vorname, nachname, klasse):
        self.cursor.execute("INSERT INTO schueler (Vorname, Nachname, klasse_id) VALUES (?,?,(SELECT id FROM klassen WHERE klasse = ?))", (vorname, nachname, klasse))
        self.conn.commit()


    def jahrgaenge_auslesen(self):
        self.cursor.execute("SELECT jahrgang FROM jahrgaenge")
        return self.cursor.fetchall()

    def klassen_auslesen(self):
        self.cursor.execute("SELECT klasse FROM klassen")
        return self.cursor.fetchall()

    def schueler_auslesen(self, klasse):
        self.cursor.execute("SELECT vorname, nachname FROM schueler JOIN klassen ON schueler.klasse_id = klassen.id WHERE klassen.klasse = ?", (klasse,))
        return self.cursor.fetchall()
    
    
    
    def db_schliessen(self):
        self.conn.close()

