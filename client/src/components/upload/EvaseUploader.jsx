import React from 'react'
import UploadPanel from './UploadPanel'

const axios = require('axios').default;

function EvaseUploader(props) {

    const cancelUpload = () => {
        props.onCancelUpload();

        let resp = null;
        axios
            .delete("/cancelupload", "UPL_CANCEL")
            .then(res => {
                resp = res.data
            })
            .catch(err => console.warn(err));

        console.log(resp)
    }

    const uploadFile = (file) => {
        console.log("Upload function triggered.")
        const formData = new FormData();
        formData.append(
            "file",
            file
        );
        let resp = null;
        axios
            .post(url="/upload", data=formData)
            .then(res => {
                resp = res.data
            })
            .catch(err => console.warn(err));

        if (resp) {
            props.onSuccessfulUpload();
        }
        return resp;
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