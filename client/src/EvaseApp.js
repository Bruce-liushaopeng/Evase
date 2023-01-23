import React, { useState } from 'react';
import Upload from './containers/Upload'
import Analysis from './containers/Analysis'

const axios = require('axios').default;



function App() {
    const [respond, setRespond] = useState("");
    const [fileUploaded, setFileUploaded] = useState(false);
    const [projectName, setProjectName] = useState("");

    const uploadFile = (projectName, file) => {
        console.log("Project name given:")
        console.log(projectName)
        console.log(typeof file)
        console.log("Upload function triggered.")
        const formData = new FormData();
        formData.append(
            "file",
            file,
            file.name
        );
        axios
            .post("http://127.0.0.1:5000/upload/"+projectName, formData)
            .then(res => {
                setRespond(res.data)
                setFileUploaded(true);
            })
            .catch(err => console.warn(err));
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

    const contentChange = () => {
        if (fileUploaded) {
            <Analysis />
        } else {
            <Upload instruction="Input your source code in ZIP format." onSubmission={uploadFile} onCancel={cancelFile} onChange={fileChanged}/>
        }
    }

    return (
        <div className="App">
            {contentChange()}
            <div className="uploadResult">
                {backendInformation()}
            </div>
        </div>
    );
}

export default App;