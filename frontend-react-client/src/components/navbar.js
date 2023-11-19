import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = ({ height }) => {
  return (
    <nav 
      className='flex items-center justify-center bg-bgColor-dark text-textColor-light navbarComponent'
      style={{ height: `${height}` }}
    > 
      <div className='flex justify-between w-full px-5 navbarContent'>
        <Link to={'/'}>
          <div className='flex space-x-4 items-center'>
            <img src='/logo512.png' alt='logo' className='h-14 w-14 p-1' />
            <p className='font-bold font-mono text-xl'>Logzilla</p>
          </div>
        </Link>
        <div className='flex space-x-12 items-center pr-10 text-lg'>
          <Link className='hover:underline underline-offset-4' to='/'>
            Upload
          </Link>
          <Link className='hover:underline underline-offset-4' to='/chat'>
            Chat
          </Link>
        </div>
      </div>
    </nav>
  );
};


export default Navbar;
