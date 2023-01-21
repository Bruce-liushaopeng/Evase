import React, { useState } from 'react'
import { DropzoneDialog } from "material-ui-dropzone"

const Upload = (props) => {

    const [selectedFile, setSelectedFile] = useState(null);
    const [isFilePicked, setIsFilePicked] = useState(false);
    const [dialogOpen, setDialogOpen] = useState(false);

    const cancelFile = (e) => {
        props.onCancel();
        setSelectedFile(null);
        setIsFilePicked(false);
    }

    const handleSubmission = (e) => {
        e.preventDefault();
        props.onSubmission(selectedFile);
    }

    const showDialog = () => {
        setDialogOpen(true);
    }

    const handleSave = (files) => {

        setDialogOpen(false);
        setSelectedFile(files[0]);
        setIsFilePicked(true);
        console.log(files);
    }

    const handleClose = () => {
        setDialogOpen(false);
    }


    return (
        <div className="flex flex-row bg-gray-200 rounded-xl shadow border p-20 align-center pl-40 min-h-screen">
            <header className="text-3xl text-gray-700 font-bold mb-5">
                <p>{props.instruction}</p>
            </header>
            <button className="neu-btn" onClick={showDialog} >
                Select file here
            </button>
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
                    <button className="neu-btn" onClick={handleSubmission}>Upload!</button>
                    <button className="neu-btn" onClick={cancelFile}>Cancel</button>
                </div>
            ) :
                <div />
            }
        </div>
    )
}

export default Upload