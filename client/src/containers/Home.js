import {Accordion, Progress} from "flowbite-react";
import {HiOutlineArrowCircleDown} from "react-icons/hi";
import Upload from "./Upload";
import Analyzer from "./Analyzer";
import React, {useEffect, useState} from "react";
import {default as axios} from "axios";

function Home() {

    const [progress, setProgress] = useState(0);
    const [respond, setRespond] = useState("");
    const [fileUploaded, setFileUploaded] = useState(true);
    const [fileAnalyzed, setFileAnalyzed] = useState(false);
    const [projectName, setProjectName] = useState("");
    const [analysisResult, setAnalysisResult] = useState(null);

    useEffect(
        () => {
            let progress = 0
            if (fileUploaded) {
                progress += 50;
            }
            if (fileAnalyzed) {
                progress += 50;
            }
            setProgress(progress);
        }, [fileUploaded, fileAnalyzed]
    );


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
        setProgress(0);
    }

    const fileChanged = () => {
        setRespond("")
        setProgress(0);
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


        <div className='max-w-[1000px] mx-auto p-4 items-start justify-center w-full h-full'>
            <div className=' sm:mt-5 w-full flex justify-center items-center flex-col mb-7'>
                <p className='text-4xl font-bold inline border-b-4 border-cyan-500 text-center '>Evase</p>
                <p className='py-4 text-2xl'>Analyze your source code for SQL Injection attack behaviours!</p>
            </div>
            <div>
                <div className="mx-50 justify-center items-center">
                    <Accordion className='mx-auto' arrowIcon={HiOutlineArrowCircleDown}>
                        <Accordion.Panel alwaysOpen={true}>
                            <Accordion.Content>
                                <Progress progress={progress}/>
                            </Accordion.Content>
                        </Accordion.Panel>
                        <Accordion.Panel alwaysOpen={true}>
                            <Accordion.Title>
                                EVASE Upload
                            </Accordion.Title>
                            <Accordion.Content>
                                <p className="mb-2 text-gray-500 dark:text-gray-400">
                                    Flowbite is an open-source library of interactive components built on top of
                                    Tailwind CSS including buttons, dropdowns, modals, navbars, and more.
                                </p>
                                <div className='pt-5 pl-5 pr-5 pb-5'>
                                    <Upload onSubmission={uploadFile} onCancel={cancelFile} onChange={fileChanged}
                                            backendInformation={backendInformation()}/>
                                </div>
                            </Accordion.Content>
                        </Accordion.Panel>
                        {fileUploaded ? (
                            <Accordion.Panel>
                                <Accordion.Title>
                                    EVASE Analyze
                                </Accordion.Title>
                                <Accordion.Content>
                                    <p className="mb-2 text-gray-500 dark:text-gray-400">
                                        Flowbite is first conceptualized and designed using the Figma software so
                                        everything you see in the library has a design equivalent in our Figma file.
                                    </p>
                                    < Analyzer/>
                                </Accordion.Content>
                            </Accordion.Panel>
                        ) : (
                            <></>
                        )}
                    </Accordion>
                </div>
            </div>
        </div>
    );
}

export default Home;