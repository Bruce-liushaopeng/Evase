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

    const handleSqlChange = (e) => {
        e.preventDefault();
        setSQLInjection(e.target.value)
    }

    const handleFDLChange = (e) => {
        e.preventDefault();
        setFDeadlock(e.target.value)
    }

    const handleNoEncChange = (e) => {
        e.preventDefault();
        setNoEnc(e.target.value)
    }

    const handlePsswdGuessingChange = (e) => {
        e.preventDefault();
        setPsswdGuessing(e.target.value)
    }

    return (
        <div className="neu-box">
            <p>Please select the types of attack behaviours to detect.</p>
            <input type="radio" id="sqlRadio" name="sqlRadio" onChange={handleSqlChange}/>
            <input type="radio" id="fdlRadio" name="fdlRadio" onChange={handleFDLChange}/>
            <input type="radio" id="nencRadio" name="nencRadio" onChange={handleNoEncChange}/>
            <input type="radio" id="psswdGuessingRadio" name="psswdGuessingRadio" onChange={handlePsswdGuessingChange}/>
            <button id="submit" name="submit" onClick={handleSubmission}/>
        </div>
    )
}

export default Analysis