import sqlite3


class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=MetaSingleton):
    def __init__(self):
        self.connection = None

    def connect(self, new=False):
        if new or self.connection is None:
            self.connection = sqlite3.connect('images.sqlite')
        return self.connection

    def get_cursor(self):
        connection = self.connect()
        try:
            cursor_obj = connection.cursor()
        except sqlite3.ProgrammingError:
            connection = self.connect(new=True)
            cursor_obj = connection.cursor()
        return connection, cursor_obj

    def create_table(self):
        connection, cursor = self.get_cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS images(
                            img_id INTEGER PRIMARY KEY,
                            image BLOB,
                            format TEXT,
                            name TEXT,
                            comment TEXT);""")
        connection.commit()
        cursor.close()
        return 1

    def insert_into_table(self, data=(None, None, None, None, None)):
        connection, cursor = self.get_cursor()
        query = """INSERT INTO images(img_id, image, format, name, comment)
                                VALUES(?,?,?,?,?);"""
        cursor.execute(query, data)
        connection.commit()
        return cursor.lastrowid

    def update_data(self, data, value, img_id):
        connection, cursor = self.get_cursor()
        query = """UPDATE images SET {}=? WHERE img_id=?;""".format(data)
        cursor.execute(query, (value, img_id))
        connection.commit()
        return cursor.lastrowid

    def get_data(self, data, img_id):
        connection, cursor = self.get_cursor()
        query = """SELECT {} FROM images WHERE img_id=?;""".format(data)
        cursor.execute(query, (img_id,))
        result = cursor.fetchall()
        cursor.close()
        return result

    def execute_query(self, query):
        connection, cursor = self.get_cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def get_lid(self):
        img_id = self.execute_query('SELECT MAX(img_id) from images')[0][0]
        if img_id is None:
            img_id = 0
        return img_id


