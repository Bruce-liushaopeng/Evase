import React, {useEffect, useState} from 'react';
import Upload from './containers/Upload'
import Analyzer from './containers/Analyzer'
import ErrorAlert from "./containers/ErrorAlert";

const axios = require('axios').default;
axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*';

function App() {
    const [respond, setRespond] = useState("");
    const [fileUploaded, setFileUploaded] = useState(false);
    const [error, setError] = useState("");
    const [info, setInfo] = useState("");
    const [showError, setShowError] = useState(false);
    const [showInfo, setShowInfo] = useState(false);

    useEffect(() => {
        const timer = setTimeout(() => {
            dismissError();
            }, 6000);
        return () => clearTimeout(timer);
    }, [showError]);

    useEffect(() => {
        const timer = setTimeout(() => {
            dismissInfo();
        }, 4000);
        return () => clearTimeout(timer);
    }, [showInfo]);

    const changeTheme = (e) => {
        e.preventDefault();
        console.log("value");

        // if set via local storage previously
        if (localStorage.getItem('color-theme')) {
            if (localStorage.getItem('color-theme') === 'light') {
                document.documentElement.classList.add('dark');
                localStorage.setItem('color-theme', 'dark');
            } else {
                document.documentElement.classList.remove('dark');
                localStorage.setItem('color-theme', 'light');
            }

            // if NOT set via local storage previously
        } else {
            if (document.documentElement.classList.contains('dark')) {
                document.documentElement.classList.remove('dark');
                localStorage.setItem('color-theme', 'light');
            } else {
                document.documentElement.classList.add('dark');
                localStorage.setItem('color-theme', 'dark');
            }
        }
    }

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
            .post("http://127.0.0.1:5000/upload/"+projectName, formData, {timeout: 1000})
            .then(res => {
                setInfo("File upload success! Commencing analysis...");
                setShowInfo(true);

                setRespond(res.data);
                setFileUploaded(true);
            })
            .catch(function (error) {
                console.log("ERROR");
                if (error.response) {
                    setError("The server could not process your request at this time. Apologies.");
                } else if (error.request) {
                    setError("The server did not receive your request at this time. Apologies.");
                } else {
                    setError("The client could not assemble your request at this time. Apologies.");
                }
                setShowError(true);
            });
    }

    const cancelFile = () => {
        setRespond("")
    }

    const fileChanged = () => {
        setRespond("")
    }

    const backendInformation = () => {
        if (fileUploaded) {
            return <p> Backend Reply: {respond}</p>
        }
    }

    const receiveError = (e) => {
        console.log(e);
        setError(e);
        setShowError(true);
    }

    const receiveInfo = (i) => {
        console.log(i);
        setInfo(i);
        setShowInfo(true);
    }

    const dismissError = () => {
        setError("");
        setShowError(false);
    }

    const dismissInfo = () => {
        setInfo("");
        setShowInfo(false);
    }

    return (
        <div className='w-full min-h-screen color1 textcolor items-start'>
            <div className="mx-auto color4">
                <button className="rounded-lg text-sm px-5 py-2.5 mx-2 mb-2 color2" onClick={changeTheme}></button>
            </div>
            <div>
                {showError ? (
                    <ErrorAlert className='my-4' message={error} high={true} onDismiss={dismissError}></ErrorAlert>
                ) : (
                    <></>
                )}
                { showInfo ? (
                    <ErrorAlert className='my-4' message={info} high={false} onDismiss={dismissInfo}></ErrorAlert>

                ) :(
                    <></>
                )
                }
            </div>
            <div className='max-w-[1500px] mx-auto'>
                <div className='float-left p-5 mt-14 w-[350px] rounded shadow-md'>
                    <img className="w-[350px] h-[350px] rounded" src="/logofile.png" />
                    <p className='mt-5 text-xl font-semibold'>Our Goals</p>
                    <p className='mt-5'>Evase is a tool that helps you analyze your Python Backend code for SQL injection vulnerabilities. The goal of Evase is to provide adequate detection of such vulnerabilites such that developers can secure their code.</p>
                </div>
                <div className='main-panel pt-16'>
                    <div className='section-panel ml-16 w-[650px] p-4'>
                        <Upload onSubmission={uploadFile} onCancel={cancelFile} onChange={fileChanged} backendInformation={backendInformation()} infoMsg={receiveInfo}/>
                    </div>
                    <div className='section-panel lg:w-[1000px] md:w-[850] ml-8 p-4'>
                        <Analyzer ready={fileUploaded} readyCallback={()=>setFileUploaded(false)} errorMsg={receiveError} infoMsg={receiveInfo}/>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default App;