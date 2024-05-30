import sqlite3

class PersistenceRegistry:
    """
    A class for managing persistence of UUIDs and HTML content in a SQLite database.

    This class provides methods for:

    * Creating and managing tables in the database.
    * Mapping UUIDs to integer IDs and vice versa.
    * Storing and retrieving HTML content associated with components.

    Attributes:
        conn (sqlite3.Connection): The connection to the SQLite database.
    """

    def __init__(self, db_file):
        """
        Initializes a new PersistenceRegistry instance.

        Args:
            db_file (str): The path to the SQLite database file.
        """

        self.conn = sqlite3.connect(db_file)
        self.create_tables()

    def create_tables(self):
        """
        Creates the necessary tables in the database if they don't already exist.

        The following tables are created:

        * `uuid_mapping`: Maps UUIDs to integer IDs.
        * `html_mapping`: Maps component IDs to HTML content.
        """

        cursor = self.conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS uuid_mapping (
                            uuid TEXT PRIMARY KEY,
                            integer_id INTEGER UNIQUE
                        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS html_mapping (
                            component_id TEXT PRIMARY KEY,
                            html_content TEXT
                        )''')

        self.conn.commit()

    def find_or_create_uuid_integer_mapping(self, uuid_str, integer_id):
        """
        Finds the existing UUID for the given integer ID, or creates a new mapping if none exists.

        Args:
            uuid_str (str): The UUID string.
            integer_id (int): The integer ID.

        Returns:
            str: The existing or newly created UUID.
        """

        existing_uuid = self.retrieve_uuid(integer_id)
        if existing_uuid:
            return existing_uuid
        return self.insert_uuid(uuid_str, integer_id)

    def insert_uuid(self, uuid_str, integer_id):
        """
        Inserts a new mapping between a UUID and an integer ID into the database.

        Args:
            uuid_str (str): The UUID string.
            integer_id (int): The integer ID.
        """

        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO uuid_mapping (uuid, integer_id)
                          VALUES (?, ?)''', (uuid_str, integer_id))
        self.conn.commit()

    def retrieve_uuid(self, integer_id):
        """
        Retrieves the UUID associated with the given integer ID.

        Args:
            integer_id (int): The integer ID.

        Returns:
            str: The UUID string, or None if no mapping exists.
        """

        cursor = self.conn.cursor()
        cursor.execute('''SELECT uuid FROM uuid_mapping
                          WHERE integer_id = ?''', (integer_id,))
        row = cursor.fetchone()
        return row[0] if row else None

    def insert_html(self, component_id, html_content):
        """
        Inserts the HTML content associated with a component into the database.

        Args:
            component_id (str): The component ID.
            html_content (str): The HTML content.
        """

        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO html_mapping (component_id, html_content)
                              VALUES (?, ?)''', (component_id, html_content))
        self.conn.commit()

    def retrive_html(self, component_id):
        """
        Retrieves the HTML content associated with a component from the database.

        Args:
            component_id (str): The component ID.

        Returns:
            str: The HTML content, or None if no content is found.
        """

        cursor = self.conn.cursor()
        cursor.execute('''SELECT uuid FROM html_mapping
                          WHERE component_id = ?''', (component_id,))
        row = cursor.fetchall()
        print("row", row)
        return row[0] if row else None

registry = PersistenceRegistry("./persistance.db")
