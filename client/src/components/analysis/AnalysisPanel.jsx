import React from 'react'

import AnalysisForm from './Analysis'

import { 
    H6,
    Button,
    withResize
} from 'ui-neumorphism'


class AnalysisPanel extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
        <>
            <AnalysisForm title="Evase Analysis Tool" subtitle="Analyze the code you uploaded."></AnalysisForm>
        </>
        );
    }
}

export default withResize(AnalysisPanel);