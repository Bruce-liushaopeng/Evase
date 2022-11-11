import React from 'react'

import { 
    Card,
    ProgressCircular,
    H6,
    Body2,
    withResize
} from 'ui-neumorphism'


class AnalysisForm extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
        <>
            <ProgressCircular
                indeterminate={true}
            />
        </>
        );
    }
}

export default withResize(AnalysisForm);