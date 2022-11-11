import React from 'react'

import UploadForm from './Upload'

import { 
    Card,
    CardContent,
    H6,
    Body2,
    withResize
} from 'ui-neumorphism'


class UploadPanel extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            uploadAttempt: false,
            currentMessage: "",
            responseMessage: ""
        };
    }

    uploadFile = (file) => {

        let result = this.props.onUpload(file)

        if (!result) {
            result = "The server didn't receive your code."
        }

        this.setState({
            uploadAttempt: true,
            currentMessage: this.props.uploadMessage,
            responseMessage: result
        });

        return result ? true : false
    }

    cancelFile = () => {
        this.setState({
            uploadAttempt: false,
            currentMessage: this.props.cancelMessage,
            responseMessage: ""
        });
    }

    fileChanged = () => {
        this.setState({
            currentMessage: this.props.changeMessage,
            responseMessage: ""
        });
    }

    render() {
        return (
            <>
                <UploadForm
                    title={this.props.title}
                    subtitle={this.props.subtitle}
                    onUpload={this.uploadFile}
                    onCancel={this.cancelFile}
                    onChange={this.fileChanged}
                />
                <CardContent>
                    <>
                    <Body2>
                        {this.state.currentMessage}
                    </Body2>
                    {this.state.uploadAttempt ? (
                        <>
                            <H6>Response Message</H6>
                            <Body2>
                                {this.state.responseMessage}
                            </Body2>
                        </>
                        ) :
                        (
                            <></>
                        )}
                    </>
                </CardContent>
            </>
        )
    }
}

export default withResize(UploadPanel);