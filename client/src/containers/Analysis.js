import React, { useState } from 'react'
import './styles.css'

const Analysis = (props) => {

    const [sqlInjection, setSQLInjection] = useState(false);
    const [fDeadlock, setFDeadlock] = useState(false);
    const [noEnc, setNoEnc] = useState(false);
    const [psswdGuessing, setPsswdGuessing] = useState(false);

    const handleSubmission = (e) => {
        e.preventDefault();
        if (!sqlInjection && !fDeadlock & !noEnc && !psswdGuessing) {
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
                    onChange={handleFDLChange}
                />
                Forced Deadlock Attack Behaviours
            </label><br/>
            <label>
                <input
                    type="radio"
                    name="nencRadio"
                    value="no_enc"
                    onChange={handleNoEncChange}
                />
                Lack of Password Encryption Attack Behaviours
            </label><br/>
            <label>
                <input
                    type="radio"
                    name="psswdGuessingRadio"
                    value="psswd_guessing"
                    onChange={handlePsswdGuessingChange}
                />
                Brute-Force Password Guessing Attack Behaviours
            </label><br/>
            <button id="submit" name="submit" onClick={handleSubmission}>Perform Analysis</button>
        </form>
    )
}

export default Analysis