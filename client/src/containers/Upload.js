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
        <div>
            <h1 className="text-3xl font-bold mb-2">
                EVASE Upload
            </h1>
            <form onSubmit={handleSubmission} onReset={cancelFile}>
                <fieldset>
                    <legend className='text-bold'>Project details</legend>
                    <label htmlFor='prjname'>Project name:</label>
                    <input type="text" id="prjname" name="prjname" className='w-30 h-8 m-4' value={projectName} onChange={handlePrjNameChange}/><br />
                    <label htmlFor='selectfile'>Project source code:</label>
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
                    <button id='selectfile' className='group container justify-center items-center w-fit m-4 py-0.5 px-2 rounded-md border small-content-div disabled:opacity-75' onClick={showDialog} >
                        Select file here
                    </button>
                    <output>
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
                    </output>
                    <output>
                        {props.backendInformation}
                    </output>
                </fieldset>
                {
                    <React.Fragment>
                        <input type='submit' className='group container justify-center items-center w-fit m-4 ml-0 py-0.5 px-2 rounded-md border small-content-div disabled:opacity-75'/>
                        <input type='reset' className='group container justify-center items-center w-fit m-4 py-0.5 px-2 rounded-md border small-content-div disabled:opacity-75'/>
                    </React.Fragment>
                }
            </form>


        </div>
    )
}

export default Upload