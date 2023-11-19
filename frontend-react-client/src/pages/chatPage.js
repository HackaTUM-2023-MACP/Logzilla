import React, { useState, createContext, useContext } from 'react';
import ChatComponent from '../components/Chat';
import SummaryBox from '../components/SummaryBox';
import TopKLogContext from '../components/TopKLogContext';



const ChatPage = ({ navbarHeight, footerHeight }) => {
  // Define the initial values for topKLogRefs and summary
  const [topKLogRefs, setTopKLogRefs] = useState([]);
  const [summary, setSummary] = useState('');

  return (
    // Wrap the JSX code with the TopKLogContext.Provider and pass the values as the value prop
    <TopKLogContext.Provider value={{ topKLogRefs, setTopKLogRefs, summary, setSummary }}>
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
    </TopKLogContext.Provider>
  );
};


export default ChatPage;
