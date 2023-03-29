import React from "react";
import { BsFileEarmarkCode } from 'react-icons/bs';
import { AiOutlineSecurityScan } from 'react-icons/ai';
import { MdOutlineTransitEnterexit } from 'react-icons/md';

const CodeReportBlockDismiss = ({moduleName, functionName, variables, endpoint, doClick}) => {

    const variablesString = (variables ? variables.join(", ") : "");
    const endpointString = (endpoint ? "True": "False");

    return (
        <div className="max-h-min w-full mx-auto my-2 color1 hover:shadow-xl text-inherit bg-inherit rounded-lg textcolor shadow-lg" >
            <div className='p-4'>
                <div className='flex flex-row justify-between'>
                    <div className='flex flex-col'>
                        <div className='cursor-pointer'>
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
                        </div>
                    </div>
                    <div>
                        <button className='rounded shadow-sm hover:shadow-md' onClick={doClick}>
                            <MdOutlineTransitEnterexit size={20} />
                        </button>
                    </div>
                </div>
                <div >
                    <details>
                        <summary className="font-semibold cursor-pointer">More info</summary>
                        <div className='pl-1 text-sm'>
                            <p>Variables: {variablesString}</p>
                            <p>Endpoint: {endpointString}</p>
                        </div>
                    </details>
                </div>
            </div>
        </div>
    );
}

export default CodeReportBlockDismiss;