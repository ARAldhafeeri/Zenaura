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
                            integer_id INTEGER UNIQUE
                        )''')

        # Table to map HTML components to UUIDs and their content
        cursor.execute('''CREATE TABLE IF NOT EXISTS html_mapping (
                            component_id TEXT PRIMARY KEY,
                            html_content TEXT
                        )''')

        self.conn.commit()
    
    def find_or_create_uuid_integer_mapping(self, uuid_str, integer_id):
        existing_uuid = self.retrieve_uuid(integer_id)
        if existing_uuid:
            return existing_uuid
        return self.insert_uuid(uuid_str, integer_id)

    def insert_uuid(self, uuid_str, integer_id):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO uuid_mapping (uuid, integer_id)
                          VALUES (?, ?)''', (uuid_str, integer_id))
        self.conn.commit()

    def retrieve_uuid(self, integer_id):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT uuid FROM uuid_mapping
                          WHERE integer_id = ?''', (integer_id,))
        row = cursor.fetchone()
        return row[0] if row else None

    def insert_html(self, component_id, html_content):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO html_mapping (component_id, html_content)
                              VALUES (?, ?)''', (component_id, html_content))
        self.conn.commit()

    def retrive_html(self, component_id):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT uuid FROM html_mapping
                          WHERE component_id = ?''', (component_id,))
        row = cursor.fetchall()
        print("row", row)
        return row[0] if row else None
registry = PersistenceRegistry("./persistance.db")