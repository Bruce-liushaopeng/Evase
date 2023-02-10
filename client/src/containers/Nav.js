import React, {useState} from 'react';
import {Button, Navbar} from 'flowbite-react';
import logo from '../assets/logofile.png';

function Nav() {

    const [index, setIndex] = useState(0);

    return (
        <Navbar
            fluid={true}
            rounded={true}
        >
            <Navbar.Brand href="https://flowbite.com/">
                <img
                    src={logo}
                    className="mr-3 h-6 sm:h-9"
                    alt="Evase Logo"
                />
                <span className="self-center whitespace-nowrap text-xl font-semibold dark:text-white">
      Evase App
    </span>
            </Navbar.Brand>
            <Navbar.Collapse>
                <Navbar.Link
                    href="/"
                    active={(index === 0)}
                    onClick={() => setIndex(0)}
                >
                    Home
                </Navbar.Link>
                <Navbar.Link
                    href="/about"
                    active={(index === 1)}
                    onClick={() => setIndex(1)}
                >
                    About
                </Navbar.Link>
                <Navbar.Link
                    href="/contact"
                    active={(index === 2)}
                    onClick={() => setIndex(2)}
                >
                    Contact
                </Navbar.Link>
            </Navbar.Collapse>
        </Navbar>
    );
}

export default Nav;