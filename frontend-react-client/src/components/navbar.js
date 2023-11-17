import React from 'react'
import {Link} from 'react-router-dom';


const Navbar = () => {
  return (
    <nav className='flex flex-col items-center justify-center'>
      <div>
        <Link className="App-link" to="/">Home</Link>
        &nbsp;|&nbsp;
        <Link className="App-link" to="/page2">Page2</Link>
      </div>
    </nav>
  )
}

export default Navbar