import React, { useState } from 'react'
import './styles.css'

const axios = require('axios').default;

const Upload = (props) => {

    const [selectedFile, setSelectedFile] = useState(null);
    const [isFilePicked, setIsFilePicked] = useState(false)

     const changeHandler = (e) => {
        e.preventDefault()
        props.onChange()
        setSelectedFile(e.target.files[0]);
        setIsFilePicked(true)
        console.log("Change to file handled.")
     }

    const cancelFile = (e) => {
        props.onCancel()
        setSelectedFile(null)
        setIsFilePicked(false)
    }

    const handleSubmission = (e) => {
        e.preventDefault()
        props.onSubmission(selectedFile)
    }


    return (
    <div className="neu-box">
        <header className="uploadInstruction">
            <p>{props.instruction}</p>
        </header>
        <input type="file" onChange={changeHandler} />
        {isFilePicked ? (
            <div>
                <p>Filename: {selectedFile.name}</p>
                <p>Filetype: {selectedFile.type}</p>
                <p>Size in bytes: {selectedFile.size}</p>
                <p>
                    Date last modified:{' '}
                    {selectedFile.lastModifiedDate.toLocaleDateString()}
                </p>
            </div>
        ) : (
            <p>Select a file to show details</p>
        )}
        {isFilePicked ? (
            <div>
                <button className="neu-btn" onClick={handleSubmission}>Upload!</button>
                <button className="neu-btn" onClick={cancelFile}>Cancel</button>
            </div>
        ) :
            <div/>
        }
	</div>
    )
}

export default Upload