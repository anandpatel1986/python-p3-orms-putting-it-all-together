import sqlite3

CONN = sqlite3.connect("lib/dogs.db")
CURSOR = CONN.cursor()


class Dog:
    all = []

    def __init__(self, name, breed, id=None):
        self.id = id
        self.name = name
        self.breed = breed

    def save(self):
        sql = """
                INSERT INTO dogs ( name, breed ) VALUES ( ?, ?)"""
        CURSOR.execute(sql, (self.name, self.breed))
        CONN.commit()
        self.id = CURSOR.execute("SELECT last_insert_rowid() FROM dogs ").fetchone()[0]

    def update(self):
        sql = """
            UPDATE dogs
            SET name = ?,
                breed = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.breed, self.id))
        CONN.commit()

    @classmethod
    def create_table(cls):
        sql = """ CREATE TABLE IF NOT EXISTS dogs (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    breed TEXT
                )"""
        CURSOR.execute(sql)

    @classmethod
    def drop_table(cls):
        sql = """ DROP TABLE IF EXISTS dogs"""
        CURSOR.execute(sql)

    @classmethod
    def create(cls, name, breed):
        dog = Dog(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, row):
        dog = cls(name=row[1], breed=row[2], id=row[0])
        return dog

    @classmethod
    def get_all(cls):
        sql = """ SELECT * FROM dogs"""
        all = CURSOR.execute(sql).fetchall()
        cls.all = [cls.new_from_db(row) for row in all]
        return cls.all

    @classmethod
    def find_by_name(cls, name):
        sql = """ SELECT * FROM dogs WHERE name = ? LIMIT 1 """
        dog = CURSOR.execute(sql, (name,)).fetchone()
        if not dog:
            return None
        else:
            return cls.new_from_db(dog)

    @classmethod
    def find_by_id(cls, id):
        sql = """ SELECT * FROM dogs WHERE id = ? LIMIT 1 """
        dog = CURSOR.execute(sql, (id,)).fetchone()
        return cls.new_from_db(dog)

    @classmethod
    def find_or_create_by(cls, name, breed):
        sql = """SELECT * FROM dogs WHERE name = ? AND breed = ? LIMIT 1"""
        dog = CURSOR.execute(sql, (name, breed)).fetchone()
        if dog:
            return cls.new_from_db(dog)
        else:
            return cls.create(name, breed)
