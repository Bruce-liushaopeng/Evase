import React, { useState } from 'react'
import { DropzoneDialog } from "material-ui-dropzone"
import './styles.css'

const Upload = (props) => {

    const [selectedFile, setSelectedFile] = useState(null);
    const [projectName, setProjectName] = useState("");
    const [isFilePicked, setIsFilePicked] = useState(false);
    const [dialogOpen, setDialogOpen] = useState(false);
    const cancelFile = (e) => {
        props.onCancel();
        setSelectedFile(null);
        setIsFilePicked(false);
    }

    const handleSubmission = (e) => {
        e.preventDefault();
        if (projectName.length === 0) {
            alert("You must input a project name.");
        } else {
            props.onSubmission(projectName, selectedFile);
            setProjectName("");
            setSelectedFile(null);
            setIsFilePicked(null);
        }
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

    const handlePrjNameChange = (e) => {
        e.preventDefault();
        setProjectName(e.target.value);
    }


    return (
        <div className="neu-box">
            <p>Please input your project name.</p>
            <input type="text" id="prjname" name="prjname" value={projectName} onChange={handlePrjNameChange}/>
            <p>Please input your source code in .zip format.</p>
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