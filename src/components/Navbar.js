import React, {useState} from 'react'
import { Link } from 'react-router-dom';
import { Button } from './Button';
import './Navbar.css';

function Navbar() {
    const [click, setClick] = useState(false); 
    const [button, setButton]=useState(true);


    const handleClick = () => setClick(!click); 
    // NOT click to be opposite to the false state setting above

    const closeMobileMenu=()=>setClick(false);

    const showButton=()=>{
        if(window.innerWidth<=960){
            setButton(false);
        } else{
            setButton(true);
        }
    };

    window.addEventListener('resize',showButton);

    return (
        <>
            <nav className="navbar">
                <div className="navbar-container">
                    <Link to="/" className="navbar-logo">
                        TECWATCH <i className="fab fa-typo3"></i>
                    </Link>
                    <div className="menu-icon" onClick={handleClick}>
                        {/* create a new function handleClick that will enable us t click the menu icon */}
                        <i className={click ? 'fas fa-times' : 'fas fa-bars'} /> 
                        {/* this toggles between navbar and closed bar */}
                    </div>
                    <ul className={click ? 'nav-menu active' : 'nav-menu'}> {/* this line makes it such that clicking the menu componenets will make the menu disappear */}
                    <li className='nav-item'>
                        <Link to='/home' className='nav-links' onClick={closeMobileMenu}>
                            Home
                        </Link>
                    </li>
                    <li className='nav-item'>
                        <Link to='/settings' className='nav-links' onClick={closeMobileMenu}>
                            Settings
                        </Link>
                    </li>
                    <li className='nav-item'>
                        <Link to='/products' className='nav-links' onClick={closeMobileMenu}>
                            Products
                        </Link>
                    </li>
                    <li className='nav-item'>
                        <Link to='/sign-up' className='nav-links-mobile' onClick={closeMobileMenu}>
                            Sign Up
                        </Link>
                    </li>
                    </ul>
                    {button && <Button buttonStyle='btn--outline'>SIGN UP</Button>} 
                    {/* 'SIGNUP' is the children being passed in*/}
                </div>
            </nav>
        </>
    )
}

export default Navbar
