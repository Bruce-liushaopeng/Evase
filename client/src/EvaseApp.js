import React, {useEffect, useState} from 'react';
import Upload from './containers/Upload'
import Analyzer from './containers/Analyzer'
import ErrorAlert from "./containers/ErrorAlert";
import PopUpCodeBlock from './containers/PopUpCodeBlock';
import JSZip from 'jszip';
import getModuleName from "./containers/ContainerUtil";

const axios = require('axios').default;
axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*';

function App() {
    const [respond, setRespond] = useState("");
    const [file, setFile] = useState(null);
    const [fileUploaded, setFileUploaded] = useState(false);
    const [extractedFiles, setExtractedFiles] = useState(new Map());
    const [error, setError] = useState("");
    const [info, setInfo] = useState("");
    const [showError, setShowError] = useState(false);
    const [showInfo, setShowInfo] = useState(false);
    const [dark, setDark] = useState(localStorage.getItem('color-theme'));
    const [displayCode, setDisplayCode] = useState(false);

    const [selectedNode, setSelectedNode] = useState(null);
    const [codeViewProps, setCodeViewProps] = useState(null);

    // dismiss error bubble after time
    useEffect(() => {
        const timer = setTimeout(() => {
            dismissError();
            }, 6000);
        return () => clearTimeout(timer);
    }, [showError]);

    // dismiss info bubble after time
    useEffect(() => {
        const timer = setTimeout(() => {
            dismissInfo();
        }, 4000);
        return () => clearTimeout(timer);
    }, [showInfo]);

    // trigger the code view when the display is not null
    useEffect(() => {
        if (codeViewProps != null) {
            setDisplayCode(true);
        } else {
            setDisplayCode(false);
        }
    }, [codeViewProps])

    // update the properties of the code view when a new node is selected
    useEffect(() => {
        const updateProps = async () => {
            if (extractedFiles.has(selectedNode)) {

                let names = getModuleName(selectedNode);
                let start = 0;
                let end = 1000;
                const cvprops = {
                    startingLine: start+1,
                    moduleName: names['module'],
                    functionName: names['func'],
                    endpoint: false,
                    variables: ['etc'],
                }

                const reader = new FileReader();

                reader.onload = async (e) => {
                    const text = (e.target.result);

                    // split file line by line
                    let allLines = text.split('\r\n');

                    // safety fallback
                    if (end > allLines.length) {
                        end = allLines.length;
                    }

                    // rejoin only the lines between start and end
                    cvprops['code'] = allLines.slice(start, end+1).join("\n");
                    setCodeViewProps(cvprops);
                }

                // Start reading the blob as text.
                await reader.readAsText(extractedFiles.get(selectedNode));
            }
        }

        // only update if there is a selected node
        if (selectedNode != null) {
            updateProps();
        }
    }, [selectedNode])

    const changeTheme = (e) => {
        e.preventDefault();

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
                    setFileUploaded(false);
                    setError("Server didn't respond with required information.")
                }
            })
            .catch(function (error) {
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

    const onAnalysisDone = async (result) => {

        // Check if the result has any vulnerabilities at all
        let vulnerable_nodes = result['graph']['total']['nodes'].filter(node => node['vulnerable'] === true);

        // if so, extract contents
        if (vulnerable_nodes.length > 0) {
            let f = file; // zip file to extract

            const zip = new JSZip();
            const files = await zip.loadAsync(f);
            files.forEach((relPath, file) => {
                if (relPath.includes(".py")) {
                    vulnerable_nodes.forEach(async function (vul_node) {
                        let namer = vul_node['id'].split(".");
                        namer.pop();
                        let altered_vul_node = namer.join(".");

                        let relpath_pkg = relPath.replace(".py", "");
                        relpath_pkg = relpath_pkg.replace("/", ".");

                        if (relpath_pkg === altered_vul_node) {
                            //console.log("FOUND MATCH FOR " + vul_node['id'] + "   " + relpath_pkg);
                            setExtractedFiles(new Map(extractedFiles.set(vul_node['id'], await file.async("blob"))));
                        }
                    });
                }
            });
        }

        // reset the state after
        setFile(null);
        //setFileUploaded(false);
    }

    const graphNodeSelected = (node) => {
        if (node === selectedNode) {
            setDisplayCode(true);
        } else {
            setSelectedNode(node);
        }
    }

    const resetProcess = () => {
        setFile(null);
        setFileUploaded(false);

        // send delete request to the backend
        let uuid = sessionStorage.getItem('uuid');
        if (uuid) {
            axios
                .post("http://127.0.0.1:5000/deletecode", {
                    'uuid': uuid,
                }, {
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                .catch(function (error) {});

            sessionStorage.removeItem('uuid');
        }
    }


    return (
        <div className='w-full min-h-screen color1 textcolor items-start'>
            
            <div className="mx-auto color4 z-50">
                <button className="rounded-lg z-50 text-sm px-5 py-2.5 mx-2 mb-2 color2" onClick={changeTheme}></button>
            </div>
            <PopUpCodeBlock display={displayCode} {...codeViewProps} onDismiss={()=>setDisplayCode(false)} dark={dark}/>
            <div className='max-w-[1500px] mx-auto'>
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
                <div className='float-left mt-14 w-[350px] '>
                    <div className='rounded p-5 shadow-lg w-full'>
                        <img className="w-[350px] h-[350px] rounded" src="/logofile.png" />
                        <p className='mt-5 text-xl font-semibold'>Our Goal</p>
                        <p className='mt-5'>Evase is a tool that helps you analyze your Python Backend code for SQL injection vulnerabilities. The goal of Evase is to provide adequate detection of such vulnerabilites such that developers can secure their code.</p>
                    </div>
                    <div className="mt-5 float-right">
                        <button className="rounded-md p-1 drop-shadow-md hover:drop-shadow-lg my-4 mr-1 color2" onClick={resetProcess}>Reset</button>
                    </div>
                </div>

                <div className='main-panel pt-16'>
                    { !fileUploaded ? (
                        <div className={`section-panel ml-16 md:w-[650px] sm:w-[400px] p-4 ${fileUploaded ? 'hidden': ''}`}>
                            <Upload onSubmission={uploadFile} onCancel={cancelFile} onChange={fileChanged} backendInformation={backendInformation()} infoMsg={receiveInfo}/>
                        </div>
                    ) : (
                        <></>
                    )
                    }
                    {
                        fileUploaded ? (
                            <div className='section-panel lg:w-[1500px] md:w-[850] ml-8 pl-4 pr-4 pb-5'>
                                <Analyzer ready={fileUploaded} readyCallback={onAnalysisDone} errorMsg={receiveError} infoMsg={receiveInfo} onNodeClick={(node)=>graphNodeSelected(node)}/>
                            </div>
                        ) : (
                            <></>
                        )
                    }

                </div>
            </div>
        </div>
    );
}

export default App;