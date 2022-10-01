import {useEffect, useState} from "react";

const Note = ({ note, handleNoteDelete }) => {
    const handleDeleteButtonClick = () => {
        handleNoteDelete(note.note_id)
    }
    return (
        <div>
            <p className="note">
                {note.created} <br/>
                {note.title} <br/>
                {note.content} <br/>
                <button onClick={handleDeleteButtonClick}>
                    Delete Note
                </button>
            </p>
        </div>
    )
}

const NoteList = ({ notes, handleNoteDelete }) => {
    return (
        <div className='notes'>
            List of Notes
            {notes.map((note, idx)=>
                <Note key={idx} note={note} handleNoteDelete={handleNoteDelete}/>
            )}
        </div>
    )
}

const AddNoteForm = ({ handleAddNote }) => {
    const [newNote, setNewNote] = useState({title:'', content:''})
    const handleButtonClick = () => {
        handleAddNote(newNote);
    }
    return (
        <div className='newNoteForm'>
            title:
            <br/>
            <input
                value={newNote.title}
                onChange={(e) => setNewNote({...newNote, title: e.target.value})}
            />
            <br/>
            content:
            <br/>
            <input
                value={newNote.content}
                onChange={(e) => setNewNote({...newNote, content: e.target.value})}
            />
            <br/>
            <button onClick={handleButtonClick}>
                Add New Note
            </button>
        </div>
    )
}

const App = ( ) => {
    const [notes, setNotes] = useState([{}])
    useEffect(() => {
        fetch("notes").then(
            res => res.json()
        ).then(
            data => {
                setNotes(data)
                console.log(data)
            }
        )
    }, [])

    async function addNote(note) {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title: note.title, content: note.content})
        }
        await fetch('notes', requestOptions)
            .then(response => response.json())
            .then(response => setNotes([...notes, response]))
    }

    async function deleteNote(noteId) {
        const requestOptions = {
            method: 'DELETE'
        }
        await fetch(`notes/${noteId}`, requestOptions)

        setNotes(notes.filter(note => note.note_id != noteId));

    }


    return (
        <div>
            <AddNoteForm handleAddNote={addNote} />
            <br/>
            <NoteList notes={notes} handleNoteDelete={deleteNote}/>

            <br/>
        </div>
    )
}

export default App;