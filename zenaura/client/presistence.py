import sqlite3

class PersistenceRegistry:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()

        # Table to map UUIDs to integers
        cursor.execute('''CREATE TABLE IF NOT EXISTS uuid_mapping (
                            uuid TEXT PRIMARY KEY,
                            integer_id INTEGER
                        )''')

        # Table to map HTML components to UUIDs and their content
        cursor.execute('''CREATE TABLE IF NOT EXISTS html_mapping (
                            component_id TEXT PRIMARY KEY,
                            html_content TEXT
                        )''')

        self.conn.commit()
    
    def insert_uuid_integer_mapping(self, uuid_str, integer_id):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO uuid_mapping (uuid, integer_id)
                          VALUES (?, ?)''', (uuid_str, integer_id))
        self.conn.commit()

    def retrieve_integer_id(self, integer_id):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT uuid FROM uuid_mapping
                          WHERE integer_id = ?''', (integer_id,))
        row = cursor.fetchone()
        return row[0] if row else None

    def insert_html_uuid_mapping(self, component_id, html_content):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO html_mapping (component_id, html_content)
                              VALUES (?, ?)''', (component_id, html_content))
        self.conn.commit()

    def retrieve_uuid_from_component_id(self, component_id):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT uuid FROM html_mapping
                          WHERE component_id = ?''', (component_id,))
        row = cursor.fetchone()
        return row[0] if row else None
registery = PersistenceRegistry("presistance.db")