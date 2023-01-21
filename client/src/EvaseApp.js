import React, { useState } from 'react';
import Upload from './containers/Upload'
import Analysis from './containers/Analysis'
import { uploadFile } from './Hooks'




function App() {
    const [respond, setRespond] = useState("");
    const [fileUploaded, setFileUploaded] = useState(false);

    const handleUpload = (file) => {
        setFileUploaded(false);
        uploadFile(file, function(response) {
            console.log("HERE IT IS");
            if (response) {
                setFileUploaded(true);
            }
            setRespond(response);
        });
    }
    const cancelFile = () => {
        setRespond("")
    }

    const fileChanged = () => {
        setRespond("")
    }

    const backendInformation = () => {
        if (respond) {
            return <p> Backend Reply: {respond}</p>
        }
    }

    const contentUpdate = () => {
        if (fileUploaded) {
            return (<Analysis instruction="Please select what types of things you want to analyze."/>);
        } else {
            return (<Upload instruction="Input your source code in ZIP format." onSubmission={handleUpload} onCancel={cancelFile} onChange={fileChanged}/>);
        }
    }

    return (
        <div className="flex flex-row bg-gray-200 rounded-xl shadow border p-20 align-center pl-40 min-h-screen">
            {contentUpdate()}
            <div className="uploadResult">
                {backendInformation()}
            </div>
        </div>
    );
}

export default App;