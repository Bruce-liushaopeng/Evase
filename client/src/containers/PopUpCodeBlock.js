import React from "react"
import { useState } from "react"

const PopUpCodeBlock = ({ display, moduleName, code }) => {
  const [showBlock, setShowBlock] = useState(display ? display : true)
  console.log(showBlock)
  const onCancelClick = () => {
    console.log("click")
    setShowBlock(false)
  }

  return showBlock ? (
    <div
      className={`mx-auto color2 w-1/3 text-inherit color5 rounded-lg textcolor-light z-10 absolute inset-x-9 inset-y-56 ring-stone-300 shadow-lg`}
    >
      <div className="flex justify-between p-4  flex-col">
        <div className="flex flex-row justify-between color1 p-2 rounded-md shadow-lg">
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
        <div className="code-container color2 mt-5 h-[380px] rounded-lg">
          <p className="p-3">
          {code}
          </p>
        </div>
      </div>
    </div>
  ) : (
    <></>
  )
}

export default PopUpCodeBlock
