import React, {useState} from 'react';
import Upload from './containers/Upload'
import Analyzer from './containers/Analyzer'

const axios = require('axios').default;
axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*';

function App() {
    const [respond, setRespond] = useState("");
    const [fileUploaded, setFileUploaded] = useState(true);
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
            .post("http://127.0.0.1:5000/upload/" + projectName, formData)
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
        if (true) {
            return <p> Backend Reply: {respond}</p>
        }
    }

    const getAnalysisResult = () => {
        return (<pre>{JSON.stringify(analysisResult, null, 2)}</pre>);
    }

    return (
        <div className='min-h-screen flex flex-col text-gray-300'>
            <div className={`grid grid-cols-'${fileUploaded ? '3' : '1'} mx-auto`}>
                <div className=''>
                    <div className='pt-5 pl-5 pr-5 pb-5'>
                    <Upload onSubmission={uploadFile} onCancel={cancelFile} onChange={fileChanged}
                            backendInformation={backendInformation()}/>
                    </div>
                    {fileUploaded ? (
                            <div className='pt-5 pl-5 pr-5 pb-5'>
                        <Analyzer/>
                            </div>
                    ) : (
                        <></>
                    )}
                </div>
            </div>
        </div>

    );
}

export default App;