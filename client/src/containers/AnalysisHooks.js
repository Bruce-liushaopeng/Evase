const {default: axios} = require("axios");

export const analyzeCode = async (sql, fdl, nenc, psswdg) => {
    const params = new URLSearchParams([['sql', sql], ['fdl', fdl], ['no_enc', nenc], ['pswd_guessing', psswdg]]);
    let result = null;
    await axios
        .get("http://127.0.0.1:5000/analyze", { params })
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