import React from 'react'

import CreditsForm from './Credits'

import { 
    H6,
    withResize
} from 'ui-neumorphism'


class CreditsPanel extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
        <div>
            <CreditsForm></CreditsForm>
        </div>
        );
    }
}

export default withResize(CreditsPanel);