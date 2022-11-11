import React  from 'react';
import HomeForm from './components/home/EvaseHome'
import EvaseCredits from './components/credits/EvaseCredits'

import {
    BrowserRouter as Router,
    Routes,
    Route,
    Link
} from "react-router-dom";


import './styles.css'
import 'ui-neumorphism/dist/index.css'


class App extends React.Component {

    render() {
        return (
            <Router>
                <Routes>
                    <Route path="/credits" element={<EvaseCredits />}></Route>
                    <Route path="/" element={<HomeForm />}></Route>
                </Routes>
            </Router>
        );
    }
}

export default App;