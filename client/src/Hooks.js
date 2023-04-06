const axios = require('axios').default;

export function uploadFile(file, callback) {
    console.log(typeof file)
    console.log("Upload function triggered.")
    const formData = new FormData();
    formData.append(
        "file",
        file,
        file.name
    );
    axios
        .post(`http://backend:5000/upload`, formData)
        .then(res => {
            console.log(res.data);
            callback(res.data);
        })
        .catch(err => console.warn(err));
}