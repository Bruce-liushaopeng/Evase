import AnalysisForm from './AnalysisForm'
import { analyzeCode } from './AnalysisHooks'
import React, {useState} from "react";

const Analyzer = (props) => {

    const [analysisResult, setAnalysisResult] = useState({});

    const getAnalysisResult = async (sql, fdl, nenc, psswdg) => {
        const res = await analyzeCode(sql, fdl, nenc, psswdg);
        console.log(res);
        setAnalysisResult(res);
    }

    const prettyResult = () => {

        return (<pre>{JSON.stringify(analysisResult, null, 2)}</pre>);
    }

    return (
      <AnalysisForm onSubmission={getAnalysisResult} analysisResult={prettyResult()}/>
    );
}

export default Analyzer;