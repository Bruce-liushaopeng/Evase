import React, { useState, useCallback } from 'react'
import { DropzoneDialog } from "material-ui-dropzone"

const Upload = ({onCancel, onSubmission, backendInformation, infoMsg}) => {

    const [selectedFile, setSelectedFile] = useState(null);
    const [projectName, setProjectName] = useState("");
    const [isFilePicked, setIsFilePicked] = useState(false);
    const [dialogOpen, setDialogOpen] = useState(false);
    const [attemptCount, setAttemptCount] = useState(0);

    const cancelFile = (e) => {
        e.preventDefault();
        onCancel();
        setSelectedFile(null);
        setIsFilePicked(false);
        setAttemptCount(0);
    }

    const handleSubmission = useCallback((e) => {
        e.preventDefault();
        setAttemptCount(attemptCount+1);
        if (projectName.length === 0) {
            infoMsg("You must name your project!");
        } else {
            onSubmission(projectName, selectedFile);
            setProjectName("");
            setSelectedFile(null);
            setIsFilePicked(null);
        }
    }, [selectedFile, projectName]);

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
        <div className="w-full text-inherit bg-inherit">
            <h1 className="text-4xl font-bold mb-2">
                EVASE Upload
            </h1>
            <p>Please input your project name.</p>
            <input type="text" id="prjname" name="prjname" className='w-30 h-8 rounded-md p-1 shadow-md my-4 color2' value={projectName} onChange={handlePrjNameChange}/>
            <p>Please input your source code in .zip format.</p>
            <div className="bg-red">
                <button className="rounded-md py-1 px-2 drop-shadow-md hover:drop-shadow-lg mr-10 my-4 color2" onClick={showDialog} >
                    Select File
                </button>
            </div>
            <DropzoneDialog
                open={dialogOpen}
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
                    <button className="rounded-md p-1 drop-shadow-md hover:drop-shadow-lg mr-10 my-4 color2" onClick={handleSubmission}>Upload!</button>
                    <button className="rounded-md p-1 drop-shadow-md hover:drop-shadow-lg mr-10 my-4 color2" onClick={cancelFile}>Cancel</button>
                </div>
            ) :
                <div />
            }
            <div>
                {backendInformation}
            </div>
        </div>
    )
}

export default Upload