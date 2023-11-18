import React, { useState, useEffect } from 'react';
import VideoComponent from '../components/VideoComponent';

const HomePage = () => {
  return (
    <div className='flex flex-col items-center justify-center'>
      <VideoComponent/>
    </div>
  )
}

export default HomePage