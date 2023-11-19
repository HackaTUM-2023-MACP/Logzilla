import React, { useState, createContext, useContext } from 'react';
import ChatComponent from '../components/Chat';
import SummaryBox from '../components/SummaryBox';



const ChatPage = ({ navbarHeight, footerHeight }) => {

  return (
    // Wrap the JSX code with the TopKLogContext.Provider and pass the values as the value prop
      <div
        className='flex flex-col items-center justify-center w-full h-full'
        style={{ height: `calc(100vh - ${navbarHeight} - ${footerHeight})` }}
      >
        <div className='grid grid-cols-3 gap-8 w-full p-20 h-full'>
          {/* SummaryBox takes 2 out of 3 columns */}
          <div className='col-span-2'>
            <SummaryBox className=''/>
          </div>
          {/* ChatComponent takes 1 out of 3 columns */}
          <div className='col-span-1'>
            <ChatComponent className='' />
          </div>
        </div>
      </div>
  );
};


export default ChatPage;
