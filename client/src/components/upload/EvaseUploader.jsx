import React from 'react'
import UploadPanel from './UploadPanel'

const axios = require('axios').default;

function EvaseUploader() {

    const uploadFile = (file) => {
        console.log("Upload function triggered.")
        const formData = new FormData();
        formData.append(
            "file",
            file,
            file.name
        );
        let resp = null;
        axios
            .post("/upload", formData)
            .then(res => {
                resp = res.data
            })
            .catch(err => console.warn(err));
        return resp;
    }

    return (
        <UploadPanel
            title="Evase Analyzer Upload"
            subtitle="Input your source code in ZIP format."
            onUpload={uploadFile}
        />
    );
}

export default EvaseUploader;