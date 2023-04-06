import React, {useMemo} from "react"
import { useState, useEffect } from "react"
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus, vs } from 'react-syntax-highlighter/dist/esm/styles/prism';
import CodeReportBlockDismiss from "./CodeReportBlockDismiss";

const PopUpCodeBlock = ({ display, moduleName, functionName, code, startingLine, dark, endpoint, variables, onDismiss }) => {

  const theme = useMemo(() => {
    if (dark) {
      return vscDarkPlus;
    } else {
      return vs;
    }
  }, [dark]);


  return (display ? (
    <div
      className={`fixed mx-auto w-full h-full top-0 left-0 flex items-center justify-center rounded-lg textcolor-light z-10 inset-x-9 inset-y-56 ring-stone-300 shadow-lg`}
    >
      <div className="flex justify-between p-4 color2 flex-col rounded-xl">
        <CodeReportBlockDismiss moduleName={moduleName} functionName={functionName} endpoint={endpoint} variables={variables} doClick={onDismiss}/>
        <div className='w-[800px]'>
          <SyntaxHighlighter className='md:max-h-[400px] lg:max-h-[600px]' language="python" showLineNumbers={true} startingLineNumber={startingLine} wrapLines={true} style={theme} >
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

export default PopUpCodeBlock;
