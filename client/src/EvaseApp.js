import React, {useEffect, useState} from 'react';
import Upload from './containers/Upload'
import Analyzer from './containers/Analyzer'
import ErrorAlert from "./containers/ErrorAlert";
import PopUpCodeBlock from './containers/PopUpCodeBlock';
import JSZip from 'jszip';

const axios = require('axios').default;
axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*';

function App() {
    const [respond, setRespond] = useState("");
    const [file, setFile] = useState(null);
    const [fileUploaded, setFileUploaded] = useState(false);
    const [extractedFiles, setExtractedFiles] = useState({});
    const [error, setError] = useState("");
    const [info, setInfo] = useState("");
    const [showError, setShowError] = useState(false);
    const [showInfo, setShowInfo] = useState(false);
    const [dark, setDark] = useState(localStorage.getItem('color-theme'));
    const [displayCode, setDisplayCode] = useState(false);
    const [displayCodeText, setDisplayCodeText] = useState("");
    const [displayCodeModuleName, setDisplayCodeModuleName] = useState("");

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
                setDark(true);
            } else {
                document.documentElement.classList.remove('dark');
                localStorage.setItem('color-theme', 'light');
                setDark(false);
            }

            // if NOT set via local storage previously
        } else {
            if (document.documentElement.classList.contains('dark')) {
                document.documentElement.classList.remove('dark');
                localStorage.setItem('color-theme', 'light');
                setDark(false);
            } else {
                document.documentElement.classList.add('dark');
                localStorage.setItem('color-theme', 'dark');
                setDark(true);
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
                if ('message' in res.data) {
                    setRespond(res.data['message']);
                } else {
                    setRespond(res.data);
                }
                if ('uuid' in res.data) {
                    sessionStorage.setItem('uuid', res.data['uuid']);
                    receiveInfo("File upload success! Commencing analysis...")
                    setFile(file);
                    setFileUploaded(true);
                } else {
                    setError("Server didn't respond with required information.")
                }
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

    const dismissCodeView = () => {

    }

    const onAnalysisDone = async (result) => {

        // Check if the result has any vulnerabilities at all
        let vulnerable_nodes = result['graph']['total']['nodes'].filter(node => node['vulnerable'] === true);
        let vulnerable_edges = result['graph']['total']['edges'].filter(edge => edge['vulnerable'] === true);


        // if so, extract contents
        if (vulnerable_nodes.length > 0) {
            let f = file; // zip file to extract

            const zip = new JSZip();
            const files = await zip.loadAsync(f);
            files.forEach((relPath, file) => {
                if (relPath.includes(".py")) {
                    console.log(relPath);
                    vulnerable_nodes.forEach(async function (vul_node) {
                        let namer = vul_node['id'].split(".");
                        namer.pop();
                        let altered_vul_node = namer.join(".");

                        let relpath_pkg = relPath.replace(".py", "");
                        relpath_pkg = relpath_pkg.replace("/", ".");

                        if (relpath_pkg === altered_vul_node) {
                            //console.log("FOUND MATCH FOR " + vul_node['id'] + "   " + relpath_pkg);
                            const newExt = {};
                            newExt[vul_node['id']] = await file.async("blob");
                            console.log(newExt);
                            await setExtractedFiles({ ...extractedFiles, ...newExt});
                        }
                    });
                }
            });
        }

        // reset the state after
        setFile(null);
        setFileUploaded(false);
    }

    const graphNodeSelected = (node) => {
        console.log(node);
        console.log(extractedFiles);
        if (node in Object.keys(extractedFiles)) {
            console.log("OOGABOOGA");
            const reader = new FileReader();

            // This fires after the blob has been read/loaded.
            reader.addEventListener('loadend', (e) => {
                const text = reader.result;
                setDisplayCodeText(text);
            });

            // Start reading the blob as text.
            reader.readAsText(extractedFiles[node]);
            setDisplayCodeModuleName(node);
            setDisplayCode(true);
        }
    }

    const dummyPythonCode = `def add_user_to_db(username: str, password: str) -> str:

    conn = sqlite3.connect('sample.db')
    conn.execute(f"INSERT INTO USER ( userName, password) VALUES ('{username}', '{password}')")
    conn.commit()
    conn.close()
    return "user [" + username + "] added auccess"
    `

    return (
        <div className='w-full min-h-screen color1 textcolor items-start'>
            
            <div className="mx-auto color4 z-50">
                <button className="rounded-lg z-50 text-sm px-5 py-2.5 mx-2 mb-2 color2" onClick={changeTheme}></button>
            </div>
            <PopUpCodeBlock display={displayCode} moduleName={displayCodeModuleName} code={displayCodeText} dark={dark} onDismiss={()=>setDisplayCode(false)}/>
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
                )}
            </div>
            <div className='max-w-[1500px] mx-auto'>
                <div className='float-left p-5 mt-14 w-[350px] rounded shadow-lg'>
                    <img className="w-[350px] h-[350px] rounded" src="/logofile.png" />
                    <p className='mt-5 text-xl font-semibold'>Our Goals</p>
                    <p className='mt-5'>Evase is a tool that helps you analyze your Python Backend code for SQL injection vulnerabilities. The goal of Evase is to provide adequate detection of such vulnerabilites such that developers can secure their code.</p>
                </div>
                <div className='main-panel pt-16'>
                    <div className='section-panel ml-16 w-[650px] p-4'>
                        <Upload onSubmission={uploadFile} onCancel={cancelFile} onChange={fileChanged} backendInformation={backendInformation()} infoMsg={receiveInfo}/>
                    </div>
                    <div className='section-panel lg:w-[1000px] md:w-[850] ml-8 p-4'>
                        <Analyzer ready={fileUploaded} readyCallback={onAnalysisDone} errorMsg={receiveError} infoMsg={receiveInfo} onNodeClick={(node)=>graphNodeSelected(node)}/>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default App;