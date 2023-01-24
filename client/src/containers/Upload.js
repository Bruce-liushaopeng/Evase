import React, { useState } from 'react'
import { DropzoneDialog } from "material-ui-dropzone"

const Upload = (props) => {

    const [selectedFile, setSelectedFile] = useState(null);
    const [projectName, setProjectName] = useState("");
    const [isFilePicked, setIsFilePicked] = useState(false);
    const [dialogOpen, setDialogOpen] = useState(false);
    const [attemptCount, setAttemptCount] = useState(0);
    const [respMsg, setRespMsg] = useState("");

    const cancelFile = (e) => {
        props.onCancel();
        setSelectedFile(null);
        setIsFilePicked(false);
        setAttemptCount(0);
    }

    const handleSubmission = (e) => {
        e.preventDefault();
        setAttemptCount(attemptCount+1);
        if (projectName.length === 0) {
            alert("You must input a project name.");
        } else {
            setRespMsg(props.onSubmission(projectName, selectedFile));
            setProjectName("");
            setSelectedFile(null);
            setIsFilePicked(null);
        }
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

    const handlePrjNameChange = (e) => {
        e.preventDefault();
        setProjectName(e.target.value);
    }


    return (
        <div className="flex flex-col items-center space-x-2 text-base m-auto">
            <h1 className="text-3xl font-bold mb-2">
                EVASE Upload
            </h1>
            <p>Please input your project name.</p>
            <input type="text" id="prjname" name="prjname" className='w-30 h-8 m-4' value={projectName} onChange={handlePrjNameChange}/>
            <p>Please input your source code in .zip format.</p>
            <div className="bg-red">
                <button className=" bg-blue-300 p-2 rounded-md" onClick={showDialog} >
                    Select file here
                </button>
            </div>
            <DropzoneDialog
                open={dialogOpen}
                acceptedFiles={['application/zip']}
                onSave={handleSave}
                showPreviews={true}
                showFileNamesInPreview={true}
                onClose={handleClose}
                submitButtonText="confirm"
                cancelButtonText="cancel"
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