import React, {useState} from 'react'
import ReactJson from 'react-json-view'

const AnalysisForm = (props) => {

    const [sqlInjection, setSQLInjection] = useState(false);
    const [fDeadlock, setFDeadlock] = useState(false);
    const [noEnc, setNoEnc] = useState(false);
    const [psswdGuessing, setPsswdGuessing] = useState(false);
    const [attempt, setAttempt] = useState(0);

    const handleSubmission = async (e) => {
        e.preventDefault();
        if (!sqlInjection && !fDeadlock && !noEnc && !psswdGuessing) {
            alert("You must select one type of attack behaviour to detect.");
        } else {
            props.onSubmission(sqlInjection, fDeadlock, noEnc, psswdGuessing);
        }
        setAttempt(attempt + 1);
    }

    const handleSQLInjectionChange = (e) => {
        setSQLInjection(!sqlInjection);
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
                <fieldset>
                    <legend>Analysis options</legend>
                    <p className='text-sm'>Please select the types of attack behaviours to detect.</p>

                    <input
                        className="w-4 h-4 text-sm bg-gray-100 border-gray-300 focus:ring-blue-500 focus:ring-2"
                        type="radio"
                        id='sql'
                        value="sql"
                        checked={sqlInjection}
                        onChange={handleSQLInjectionChange}
                    />
                    <label htmlFor='sql' className="ml-2 text-sm font-medium">SQL Injection Attack Behaviours</label><br/>
                    <input type='submit'
                           className='group container justify-center items-center w-fit m-4 ml-0 py-0.5 px-2 rounded-md border small-content-div disabled:opacity-75'/><br/>
                    <output>
                        <label htmlFor='analysisresult'>Analysis result:</label>
                        <div id='analysisresult' className='text-gray-300'>
                            {resultView()}
                        </div>
                    </output>
                </fieldset>
            </form>

        </div>
    )
}

export default AnalysisForm