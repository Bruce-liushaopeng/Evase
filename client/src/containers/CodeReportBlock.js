import React from "react";
import { BsFileEarmarkCode } from 'react-icons/bs';
import { AiOutlineSecurityScan } from 'react-icons/ai';

const CodeReportBlock = ({moduleName, functionName, startLine, endLine, variables, calls, endpoint, doClick}) => {

    const variablesString = (variables ? variables.join(", ") : "");
    const endpointString = (endpoint ? "True": "False");

    return (
        <div className="max-h-min w-full mx-auto my-2 color1 hover:shadow-xl text-inherit bg-inherit rounded-lg textcolor shadow-lg" >
            <div className='p-4'>
                <div onClick={doClick}>
                    <div>
                        <span className='inline-flex'>
                            <BsFileEarmarkCode size={20}></BsFileEarmarkCode>
                            <p className='font-bold text-md ml-1 textcolor'>{moduleName}</p>
                        </span>
                    </div>
                    <div>
                        <span className='inline-flex'>
                            <AiOutlineSecurityScan size={20}></AiOutlineSecurityScan>
                            <p className='font-semibold text-sm ml-1 textcolor'>{functionName}</p>
                        </span>
                    </div>
                    <p className='my-1 text-md'>Lines: {startLine} to {endLine}</p>
                </div>

                <div >
                    <details>
                        <summary className="font-semibold">More info</summary>
                        <div className='pl-1 text-sm'>
                            <p>Variables: {variablesString}</p>
                            <p>Calls: {calls}</p>
                            <p>Endpoint: {endpointString}</p>
                        </div>
                    </details>
                </div>
            </div>

        </div>
    );
}

export default CodeReportBlock;