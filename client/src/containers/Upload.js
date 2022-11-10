import React, { useState } from 'react'
import { DropzoneDialog } from "material-ui-dropzone"
import { Button } from 'ui-neumorphism'

const Upload = (props) => {

    const [selectedFile, setSelectedFile] = useState();
    const [isFilePicked, setIsFilePicked] = useState(false)
    const [dialogOpen, setDialogOpen] = useState(false)

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

    const showDialog = () => {
        setDialogOpen(true)
    }

    const handleSave = (files) => {
        setDialogOpen(false)
        setSelectedFile(files[0])
        setIsFilePicked(true)
        console.log(files)
    }

    const handleClose = () => {
        setDialogOpen(false)
    }


    return (
        <div>
            <header className="uploadInstruction">
                <p>{props.instruction}</p>
            </header>
            <Button onClick={showDialog} >
                Select file here
            </Button>
            <DropzoneDialog
                open={dialogOpen}
                onSave={handleSave}
                showPreviews={true}
                onClose={handleClose}
                submitButtonText="Confirm"
                filesLimit={1}
                maxFileSize={500000000}
            />
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
                <div />
            }
        </div>
    )
}

export default Upload