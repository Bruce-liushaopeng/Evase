import React, { useState } from 'react'

import './styles.css'

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

    return (
        <div className="neu-box">
            <form onSubmit={handleSubmission}>
                <p>Please select the types of attack behaviours to detect.</p>
                <label>
                    <input
                        type="radio"
                        name="sqlRadio"
                        value="sql"
                        checked={sqlInjection}
                        onChange={handleSQLInjectionChange}
                    />
                    SQL Injection Attack Behaviours
                </label><br/>
                <label>
                    <input
                        type="radio"
                        name="fdlRadio"
                        value="fdl"
                        checked={fDeadlock}
                        onChange={handleFDLChange}
                    />
                    Forced Deadlock Attack Behaviours
                </label><br/>
                <label>
                    <input
                        type="radio"
                        name="nencRadio"
                        value="no_enc"
                        checked={noEnc}
                        onChange={handleNoEncChange}
                    />
                    Lack of Password Encryption Attack Behaviours
                </label><br/>
                <label>
                    <input
                        type="radio"
                        name="psswdGuessingRadio"
                        value="psswd_guessing"
                        checked={psswdGuessing}
                        onChange={handlePsswdGuessingChange}
                    />
                    Brute-Force Password Guessing Attack Behaviours
                </label><br/>
                <button className="neu-btn" id="submit" name="submit" onClick={handleSubmission}>Perform Analysis</button>
            </form>
            <div>
                <p>Analysis Result</p>
                {props.analysisResult}
            </div>
        </div>
    )
}

export default AnalysisForm