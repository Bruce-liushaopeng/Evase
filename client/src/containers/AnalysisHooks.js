const {default: axios} = require("axios");

export const analyzeCode = async () => {
    const params = new URLSearchParams();
    let result = null;
    await axios
        .get("http://127.0.0.1:5000/analyze")
        .then(res => {
            if (res.data) {
                result = res.data;
            }
        })
        .catch(err => console.warn(err));
    console.log("HOOK called.")
    console.log(result);
    return result;
}