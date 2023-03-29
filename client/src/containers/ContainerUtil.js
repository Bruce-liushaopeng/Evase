const getModuleName = function(fullName, fnSep=":") {
    let spl = fullName.split(fnSep);
    let fn_name = spl.pop();
    return {
        module: spl.join("."),
        func: fn_name
    }
}

export default getModuleName;