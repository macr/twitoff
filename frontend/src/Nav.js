import React from 'react';
import {Link} from 'react-router-dom'

function Nav(){
    return(
        <nav className='main-nav'>
            <ul>
               
                    <h1> <Link to='/'>Home </Link></h1>
               
            </ul>
        </nav>
    )
}
export default Nav;