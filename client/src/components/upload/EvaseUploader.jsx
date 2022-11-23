import React from 'react'
import UploadPanel from './UploadPanel'

const axios = require('axios').default;

function EvaseUploader(props) {

    const cancelUpload = () => {
        console.log("EvaseUploader: Cancel function triggered.")
        axios
            .delete("/cancelupload", "UPL_CANCEL")
            .catch(err => console.warn(err));

        props.onCancelUpload();
    }

    const uploadFile = async (file) => {
        console.log("EvaseUploader: Upload function triggered.")
        const formData = new FormData();
        formData.append(
            "file",
            file,
            file.name
        );
        const res = await axios
            .post("/upload", formData)
            .catch(err => {
                console.log("ERROR")
                console.warn(err)
            });

        if (res.data) {
            props.onSuccessfulUpload();
        }

        return await res.data;
    }

    return (
        <UploadPanel
            title="Evase Analyzer Upload"
            subtitle="Input your source code in ZIP format."
            onUpload={uploadFile}
            onCancel={cancelUpload}
        />

        
    );
}

export default EvaseUploader;