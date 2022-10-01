import sqlite3
from flask import Flask, request

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Get Notes API Route
#todo: make METHOD = GET for a rest api like call, change getNotes to notes
@app.route("/notes", methods = ['GET'])
def getNotes():
    notes = []
    try:
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM notes")
        rows = cur.fetchall()

        # convert row objects to dictionary
        for row in rows:
            note = {}
            note["note_id"] = row["note_id"]
            note["created"] = row["created"]
            note["title"] = row["title"]
            note["content"] = row["content"]
            notes.append(note)
    except:
        notes = []
    return notes


@app.route("/notes", methods = ['POST'])
def addNote():
    return insertNote(request.get_json())

@app.route("/notes/<noteId>", methods = ['DELETE'])
def deleteNote(noteId):
    success = deleteNoteById(noteId)
    if (success): return "", 200
    return "", 400

#========= helpers
def getNoteById(noteId):
    note = {}
    try:
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM notes WHERE note_id = ?",
                       (noteId,))
        row = cur.fetchone()

        # convert row object to dictionary
        note["note_id"] = row["note_id"]
        note["created"] = row["created"]
        note["title"] = row["title"]
        note["content"] = row["content"]
    except:
        note = {}

    return note

def deleteNoteById(noteId):
    try:
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("DELETE FROM notes WHERE note_id = ?",
                       (noteId,))
        conn.commit()
    except:
        return False

    return True

def insertNote(note):
    inserted_note = {}
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO notes (title, content) VALUES (?, ?)",
                    (
                        note['title'],
                        note['content']
                    ))
        conn.commit()
        inserted_note = getNoteById(cur.lastrowid)
    except:
        conn().rollback()

    finally:
        conn.close()

    return inserted_note

if __name__ == "__main__":
    app.run(debug=True)