import React, { useState } from 'react'
import ReactJson from 'react-json-view'

const AnalysisForm = (props) => {

    const handleSubmission = async (e) => {
        e.preventDefault();
        props.onSubmission();
    }

    const resultView = () => {
        if (props.analysisResult) {
            //return (<ReactJson src={props.analysisResult} />);
            return props.analysisResult;
        } else {
            return (<></>);
        }
    }

    return (
        <div>
            <h1 className="text-3xl font-bold mb-2">
                EVASE Analyzer
            </h1>
            <p>Click the button below to start the analysis of your code.</p>
            <button className="bg-sky-300 rounded-md p-1 hover:bg-sky-500 shadow-md" id="submit" name="submit" onClick={handleSubmission}>Perform Analysis</button>
            <div>
                <p>Analysis Result</p>
                {resultView()}
            </div>
        </div>
    )
}

export default AnalysisForm