import React, { useState } from 'react'

const axios = require('axios').default;

const Upload = (props) => {

    const [selectedFile, setSelectedFile] = useState();
    const [isFilePicked, setIsFilePicked] = useState(false)

     const changeHandler = (e) => {
        e.preventDefault()
        props.onChange()
        setSelectedFile(e.target.files[0]);
        setIsFilePicked(true)
        console.log("Change to file handled.")
     }

    const cancelFile = (e) => {
        e.preventDefault()
        props.onCancel()
        setSelectedFile(null)
        setIsFilePicked(false)
    }

    const handleSubmission = (e) => {
        e.preventDefault()

        props.onSubmission(selectedFile)
    }


    return (
    <div>
        <header className="uploadInstruction">
            <p>{props.instruction}</p>
        </header>
        <input type="file" name="file" onChange={changeHandler} />
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
                <button onClick={handleSubmission}>Upload!</button>
                <button onClick={cancelFile}>Cancel</button>
            </div>
        ) :
            <div/>
        }
	</div>
    )
}

export default Upload