import React, { useState } from 'react';
import Upload from './containers/Upload'
import Analyzer from './containers/Analyzer'

const axios = require('axios').default;
axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*';

function App() {
    const [respond, setRespond] = useState("");
    const [fileUploaded, setFileUploaded] = useState(false);
    const [projectName, setProjectName] = useState("");
    const [analysisResult, setAnalysisResult] = useState(null);

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

    const getAnalysisResult = () => {


        return (<pre>{JSON.stringify(analysisResult, null, 2)}</pre>);
    }

    const contentChange = () => {
        if (fileUploaded) {
            console.log("ANALYSIS TIME")
            return (<Analyzer />);
        } else {
            return (<Upload onSubmission={uploadFile} onCancel={cancelFile} onChange={fileChanged}/>);
        }
    }

    return (
        <div className="flex items-center space-x-2 text-base bg-green-300">
            {contentChange()}
            <div className="flex items-center space-x-2 text-base">
                {backendInformation()}
            </div>
        </div>
    );
}

export default App;