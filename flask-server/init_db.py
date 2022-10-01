import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO notes (title, content) VALUES (?, ?)",
            ('First Note', 'Content for the first note')
            )

cur.execute("INSERT INTO notes (title, content) VALUES (?, ?)",
            ('Second Note', 'Content for the second note')
            )

connection.commit()
connection.close()
