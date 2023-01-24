import React, { useState } from 'react'
import ReactJson from 'react-json-view'

const AnalysisForm = (props) => {

    const [sqlInjection, setSQLInjection] = useState(false);
    const [fDeadlock, setFDeadlock] = useState(false);
    const [noEnc, setNoEnc] = useState(false);
    const [psswdGuessing, setPsswdGuessing] = useState(false);

    const handleSubmission = async (e) => {
        e.preventDefault();
        if (!sqlInjection && !fDeadlock && !noEnc && !psswdGuessing) {
            alert("You must select one type of attack behaviour to detect.");
        } else {
            props.onSubmission(sqlInjection, fDeadlock, noEnc, psswdGuessing);
        }
    }

    const handleSQLInjectionChange = (e) => {
        setSQLInjection(!sqlInjection);
    }

    const handleFDLChange = (e) => {
        setFDeadlock(!fDeadlock);
    }

    const handleNoEncChange = (e) => {
        setNoEnc(!noEnc);
    }

    const handlePsswdGuessingChange = (e) => {
        setPsswdGuessing(!psswdGuessing);
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
            <form onSubmit={handleSubmission}>
                <p>Please select the types of attack behaviours to detect.</p>
                <label className="ml-2 text-sm font-medium text-gray-900 dark:text-black-300">
                    <input
                        className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
                        type="radio"
                        name="sqlRadio"
                        value="sql"
                        checked={sqlInjection}
                        onChange={handleSQLInjectionChange}
                    />
                    SQL Injection Attack Behaviours
                </label><br/>
                <label className="ml-2 text-sm font-medium text-gray-900 dark:text-black-300">
                    <input
                        className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
                        type="radio"
                        name="fdlRadio"
                        value="fdl"
                        checked={fDeadlock}
                        onChange={handleFDLChange}
                    />
                    Forced Deadlock Attack Behaviours
                </label><br/>
                <label className="ml-2 text-sm font-medium text-black-900 dark:text-black-300">
                    <input
                        className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
                        type="radio"
                        name="nencRadio"
                        value="no_enc"
                        checked={noEnc}
                        onChange={handleNoEncChange}
                    />
                    Lack of Password Encryption Attack Behaviours
                </label><br/>
                <label className="ml-2 text-sm font-medium text-black-900 dark:text-black-300">
                    <input
                        className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
                        type="radio"
                        name="psswdGuessingRadio"
                        value="psswd_guessing"
                        checked={psswdGuessing}
                        onChange={handlePsswdGuessingChange}
                    />
                    Brute-Force Password Guessing Attack Behaviours
                </label><br/>
                <br />
                <button className="bg-sky-300 rounded-md p-1 hover:bg-sky-500 shadow-md" id="submit" name="submit" onClick={handleSubmission}>Perform Analysis</button>
            </form>
            <div>
                <p>Analysis Result</p>
                {resultView()}
            </div>
        </div>
    )
}

export default AnalysisForm