import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = ({ height }) => {
  return (
    <nav 
      className='flex items-center justify-center bg-bgColor-dark text-textColor-light'
      style={{ height: `${height}` }}
    >
      <div className='flex space-x-4'>
        <Link className='App-link' to='/'>
          Upload
        </Link>
        <span className='text-borderColor-dark'>|</span>
        <Link className='App-link' to='/chat'>
          Chat
        </Link>
      </div>
    </nav>
  );
};


export default Navbar;
