import React, { useState, useEffect } from 'react';
import UploadBox from '../components/UploadBox';

const HomePage = ({ navbarHeight, footerHeight }) => {
  return (
    <div 
      className='flex flex-col items-center justify-center' 
      style={{ height: `calc(100vh - ${navbarHeight} - ${footerHeight})` }}
    >
      <UploadBox/>
    </div>
  )
}

export default HomePage;
