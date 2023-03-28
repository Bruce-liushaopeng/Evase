import React from "react";

const CodeReportBlock = ({moduleName, functionName, startLine, endLine, variables, calls, endpoint, doClick}) => {

    const getVarString = () => {
        if (variables) {
            return variables.join(", ");
        } else {
            return "";
        }
    }

    const getEndpointString = () => {
        return (endpoint ? "True": "False");
    }

    return (
        <div className="max-h-min w-full mx-auto my-2 color1 hover:shadow-xl text-inherit bg-inherit rounded-lg textcolor shadow-lg" >
            <div className='p-4'>
                <div onClick={doClick}>
                    <p className='font-bold text-md textcolor'>Module: {moduleName}</p>
                    <p className='font-semibold text-sm textcolor'>Function: {functionName}</p>
                    <p className='my-1 text-md'>Lines: {startLine} to {endLine}</p>

                </div>
                <div>
                    <details>
                        <summary className="font-semibold">More info</summary>
                        <div className='pl-1 text-sm'>
                            <p>Variables: {getVarString()}</p>
                            <p>Calls: {calls}</p>
                            <p>Endpoint: {endpoint}</p>
                        </div>

                    </details>
                </div>
            </div>

        </div>
    );
}

export default CodeReportBlock;