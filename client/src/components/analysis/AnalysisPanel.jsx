import React from 'react'

import AnalysisForm from './Analysis'

import { 
    H6,
    withResize
} from 'ui-neumorphism'


class AnalysisPanel extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
        <>
            <H6>Evase Analysis Tool</H6>
            <AnalysisForm></AnalysisForm>
        </>
        );
    }
}

export default withResize(AnalysisPanel);