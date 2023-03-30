export const getModuleName = function(fullName, fnSep=":") {
    let spl = fullName.split(fnSep);
    let fn_name = spl.pop();
    return {
        module: spl.join("."),
        func: fn_name
    }
}

const MAX_LINES = 30;
const LINE_BUFFER = 5;

export const getNodeProperties = function(nodeObj) {
    let data = nodeObj['__node_data'];
    // moduleName, functionName, startLine, endLine, variables, calls, endpoint

    let names = getModuleName(nodeObj['id'])
    let moduleName = names['module'];
    let funcName = names['func'];
    let endpoint = data[0]['endpoint'];
    let startLine = 0;

    let variables = [];
    let calls = [];

    let call_lines = [];

    let scope = data[0]['func_scope'];

    data.forEach(function (data_point) {
        data_point['vars'].forEach(function (v) {
            variables.push(v);
        })
        calls.push(data_point['calls_vulnerable']['name']);
        call_lines.push(parseInt(data_point['calls_vulnerable']['end']));
    });

    startLine = parseInt(scope['start']) - LINE_BUFFER;
    if (startLine < 0) {
        startLine = parseInt(scope['start']);
    }

    let endLine = parseInt(scope['end']) + LINE_BUFFER;

    if (endLine - startLine > MAX_LINES) {
        let maxCall = Math.max(...call_lines);
        endLine = maxCall + LINE_BUFFER;
        if (endLine - startLine > MAX_LINES) {
            endLine = startLine + MAX_LINES;
        }
    }

    let props = {
        moduleName: moduleName,
        functionName: funcName,
        variables: variables,
        calls: calls,
        endpoint: endpoint,
        endLine: endLine,
        startingLine: startLine
    }

    return props;
}