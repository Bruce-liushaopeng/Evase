const {default: axios} = require("axios");

/**
 * Uploads a project file to the backend.
 *
 * @param projectName The name of the project repository
 * @param file The compressed file blob
 * @returns {Promise<AxiosResponse<any>>} Promise of the request
 */
export const uploadFile = (projectName, file) => {

        const formData = new FormData();
        formData.append(
            "file",
            file,
            file.name
        );
        return axios
            .post("http://127.0.0.1:5000/upload/"+projectName, formData, {timeout: 1000})
}

/**
 * Get the contents of a log from an analysis.
 *
 * @param uuid The unique identifier for the project repository
 * @returns {Promise<AxiosResponse<any>>} Promise of the request
 */
export const getLogContents = (uuid) => {
    return axios.post("http://127.0.0.1:5000/analysislog",
            {
                'uuid': uuid
            },
            {
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        )
}

/**
 * Perform analysis and retrieve results.
 *
 * @param uuid The unique identifier for the project repository
 * @returns {Promise<AxiosResponse<any>>} Promise of the request
 */
export const getAnalysisResult = (uuid) => {
    return axios.post("http://127.0.0.1:5000/analyze", {
        'uuid': uuid,
    }, {
        headers: {
            'Content-Type': 'application/json'
        }
    })
}

