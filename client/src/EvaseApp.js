import React, { useState } from 'react';
const axios = require('axios').default;
function App() {
    const [file, setFile] = useState(null);
    const [fileName, setFileName] = useState(null);
    const [respond, setRespond] = useState("");

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
        console.log("handled")
        setFileName(e.target.files[0].name);
    }

    const cancelFile = (e) => {
        setFile(null)
        setFileName('')
    }

    const uploadFile = (e) => {
        console.log("uplaod function trigger")
        e.preventDefault()
        const formData = new FormData();
        formData.append(
            "file",
            file,
            fileName
        );
        axios
            .post("/upload", formData)
            .then(res => {
                setRespond(res.data)
            })
            .catch(err => console.warn(err));
    }

    function fileData() {
        if (!file) {
            return <p> No File Uploaded Yet</p>
        } else {
            console.log(file)
            return <p> File ready for upload:  {file.name}</p>
        }
    }

    function backendInfomation() {
        if (respond) {
            return <p> Backend Reply: {respond}</p>
        }
    }

    return (
        <div className="App">
            <header className="App-header">

                <p>Please choose the project file in zip.</p>
            </header>
            <input type="file" name="file" onChange={handleFileChange} />
            <button onClick={cancelFile}>
                cancel
            </button>
            <button onClick={uploadFile}>
                Upload!
            </button>
            <div>
                {fileData()}
            </div>
            <div>
                {backendInfomation()}
            </div>
        </div>
    );
}

export default App;