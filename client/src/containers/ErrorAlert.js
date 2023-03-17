import React from "react";

const ErrorAlert = ({message, high, onDismiss}) => {

    return (
        <div className={`h-[80px] w-[1500px] mx-auto ${high ? 'color3' : 'color2'} text-inherit bg-inherit rounded-lg textcolor-light`}>
            <div className='flex justify-between p-4 my-4 '>
                <div>
                    <p className='font-semibold text-lg textcolor'>{high ? 'Error':'Info'}</p>
                    <p className='textcolor'>{message}</p>
                </div>
                <button className='py-2 px-4 rounded-lg color4' onClick={()=>onDismiss()}>X</button>
            </div>

        </div>
    );
}

export default ErrorAlert;