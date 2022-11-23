import { useState } from 'react'

import UploadForm from './Upload'

import { 
    Card,
    CardContent,
    H6,
    Body2,
    withResize
} from 'ui-neumorphism'


function UploadPanel(props) {

    const [uploadAttempt, setUploadAttempt] = useState(false);
    const [currentMessage, setCurrentMessage] =  useState("");
    const [responseMessage, setResponseMessage] = useState("");

    const uploadFile = async (file) => {
        console.log("UploadPanel: Upload function triggered.")
        let result = await props.onUpload(file)

        if (!result) {
            result = "The server didn't receive your code."
        }

        setUploadAttempt(true);
        setCurrentMessage(props.uploadMessage);
        setResponseMessage(result);

        return result ? true : false
    }

    const cancelFile = () => {
        console.log("UploadPanel: Cancel function triggered.")
        props.onCancel();

        setUploadAttempt(false);
        setCurrentMessage(props.cancelMessage);
        setResponseMessage("");
    }

    const fileChanged = () => {
        setCurrentMessage(props.changeMessage);
        setResponseMessage("");
    }

    return (
        <>
            <UploadForm
                title={props.title}
                subtitle={props.subtitle}
                onUpload={uploadFile}
                onCancel={cancelFile}
                onChange={fileChanged}
            />
            <CardContent>
                <>
                <Body2>
                    {currentMessage}
                </Body2>
                {uploadAttempt ? (
                    <>
                        <H6>Response Message</H6>
                        <Body2>
                            {responseMessage}
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

export default UploadPanel;