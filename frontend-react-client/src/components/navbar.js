import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = ({ height }) => {
  return (
    <nav 
      className='flex items-center justify-center bg-bgColor-dark text-textColor-light'
      style={{ height: `${height}` }}
    > 
      <div className='flex items-center justify-between w-full max-w-3xl px-5'>
        <div className='flex space-x-4 items-center'>
          <img src='/logo512.png' alt='logo' className='h-14 w-14 p-1' />
          <p className='font-bold font-mono text-xl'>Logzilla</p>
        </div>
        <div className='flex space-x-12 items-center pr-10'>
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
