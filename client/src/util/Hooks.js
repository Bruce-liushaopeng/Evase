const {default: axios} = require("axios");

// if the app is running in docker, we use the ENV defined in docker
// otherwise the fixed port is used
const BACKEND_PORT = process.env.REACT_APP_BACKEND_PORT || '5050'
const BACKEND_URL = `http://localhost:${BACKEND_PORT}`

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
            .post(`${BACKEND_URL}/upload/${projectName}`, formData, {timeout: 1000})
}

/**
 * Get the contents of a log from an analysis.
 *
 * @param uuid The unique identifier for the project repository
 * @returns {Promise<AxiosResponse<any>>} Promise of the request
 */
export const getLogContents = (uuid) => {
    return axios.post(`${BACKEND_URL}/analysislog`,
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
    return axios.post(`${BACKEND_URL}/analyze`, {
        'uuid': uuid,
    }, {
        headers: {
            'Content-Type': 'application/json'
        }
    })
}

