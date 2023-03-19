import React from "react"
import { useState } from "react"
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus, vs } from 'react-syntax-highlighter/dist/esm/styles/prism';

const PopUpCodeBlock = ({ display, moduleName, code, dark, ref }) => {



  const [showBlock, setShowBlock] = useState(display)
  console.log(showBlock)
  const onCancelClick = () => {
    console.log("click")
    setShowBlock(false)
  }

  return (
    <div
      className={`fixed mx-auto w-full h-full top-0 left-0 ${showBlock ? '': 'hidden'} flex items-center justify-center rounded-lg textcolor-light z-10 inset-x-9 inset-y-56 ring-stone-300 shadow-lg`}
    >
      <div className="flex justify-between p-4 color2 flex-col rounded-xl">
        <div className="flex flex-row justify-between color1 p-2 rounded-md shadow-lg" ref={ref}>
          <div>
            <p className="textcolor font-mono text-lg">{moduleName} </p>
          </div>
          <div className="justify-end flex round">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={1.5}
              stroke="currentColor"
              onClick={onCancelClick}
              className="w-6 h-6 shadow-md color1 textcolor rounded-md hover:outline-1 cursor-pointer hover:"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M9.75 9.75l4.5 4.5m0-4.5l-4.5 4.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
          </div>
        </div>
        <SyntaxHighlighter language="python" style={dark ? vscDarkPlus : vs} wrapLines={true}>
          {code}
        </SyntaxHighlighter>
      </div>
    </div>
  )
}

export default PopUpCodeBlock
