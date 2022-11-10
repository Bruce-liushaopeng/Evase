import React, { useState } from 'react';
import Upload from './containers/Upload'

const axios = require('axios').default;



function App() {
    const [respond, setRespond] = useState("");

    const uploadFile = (file) => {
        console.log("Upload function triggered.")
        const formData = new FormData();
        formData.append(
            "file",
            file,
            file.name
        );
        axios
            .post("/upload", formData)
            .then(res => {
                setRespond(res.data)
            })
            .catch(err => console.warn(err));
    }

    const cancelFile = () => {
        setRespond("")
    }

    const fileChanged = () => {
        setRespond("")
    }

    function backendInformation() {
        if (respond) {
            return <p> Backend Reply: {respond}</p>
        }
    }

    return (
        <div className="App">
            <Upload instruction="Input your source code in ZIP format." onSubmission={uploadFile} onCancel={cancelFile} onChange={fileChanged}/>
            <div className="uploadResult">
                {backendInformation()}
            </div>
        </div>
    );
}

export default App;