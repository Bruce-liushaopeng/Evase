import React from "react"
import { useState } from "react"
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus, vs } from 'react-syntax-highlighter/dist/esm/styles/prism';
import CodeReportBlockDismiss from "./CodeReportBlockDismiss";

const PopUpCodeBlock = ({ display, moduleName, functionName, code, startingLine, dark, endpoint, variables, ref, onDismiss }) => {

  const onCancelClick = () => {
    onDismiss();
  }

  return (display ? (
    <div
      className={`fixed mx-auto w-full h-full top-0 left-0 flex items-center justify-center rounded-lg textcolor-light z-10 inset-x-9 inset-y-56 ring-stone-300 shadow-lg`}
    >
      <div className="flex justify-between p-4 color2 flex-col rounded-xl">
        <CodeReportBlockDismiss moduleName={moduleName} functionName={functionName} endpoint={endpoint} variables={variables} doClick={onDismiss}/>
        <div className='w-[800px]'>
          <SyntaxHighlighter language="python" showLineNumbers={true} startingLineNumber={startingLine} wrapLines={true} style={dark ? vscDarkPlus : vs} customStyle={{'maxHeight':'800px', 'minWidth': '100%'}}>
            {code}
          </SyntaxHighlighter>
        </div>
      </div>
    </div>
      ) : (
          <></>
      )
  )
}

export default PopUpCodeBlock
