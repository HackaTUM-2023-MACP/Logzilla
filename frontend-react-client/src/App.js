import React, { useState } from 'react';
import { BrowserRouter, Link, Routes, Route } from 'react-router-dom';
import './App.css';
import HomePage from './pages/homePage';
import ChatPage from './pages/chatPage';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import TopKLogContext from './components/TopKLogContext';


function App() {

  // Define the initial values for topKLogRefs and summary
  const [topKLogRefs, setTopKLogRefs] = useState([]);
  const [summary, setSummary] = useState('');
  const [logFileName, setLogFileName] = useState('');
  
  const navbarHeight = "52px";
  const footerHeight = "48px";
  
  return (
    <div className="bg-background min-h-screen">
      <BrowserRouter className="flex h-full w-full justify-center items-center"> 
        <TopKLogContext.Provider value={{ topKLogRefs, setTopKLogRefs, summary, setSummary, logFileName, setLogFileName }}>
          <Navbar height={navbarHeight}/>
          <Routes>
            <Route path="/" element={<HomePage navbarHeight={navbarHeight} footerHeight={footerHeight}/>} />
            <Route path="/chat" element={<ChatPage navbarHeight={navbarHeight} footerHeight={footerHeight}/>} />
          </Routes>
          <Footer height={footerHeight}/>
        </TopKLogContext.Provider>
      </BrowserRouter>
    </div>
  );
}

export default App;


