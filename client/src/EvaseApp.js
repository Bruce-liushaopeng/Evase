import React, {useState, useEffect} from 'react';

import {BrowserRouter, Route, Routes} from 'react-router-dom';
import Home from "./containers/Home";
import About from "./containers/About";
import Contact from "./containers/Contact";
import Nav from "./containers/Nav";

const axios = require('axios').default;
axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*';

function App() {

    return (

        <BrowserRouter>
            <Nav/>
            <div className="h-screen w-full text-gray-300 bg-[#0a192f]">
                <Routes>
                    <Route index element={<Home/>}/>
                    <Route path='/about' element={<About/>}/>
                    <Route path='/contact' element={<Contact/>}/>
                </Routes>
            </div>
        </BrowserRouter>
    );
}

export default App;