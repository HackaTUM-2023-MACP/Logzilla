import React from 'react';
import { BrowserRouter, Link, Routes, Route } from 'react-router-dom';
import './App.css';
import HomePage from './pages/homePage';
import ChatPage from './pages/chatPage';
import Navbar from './components/Navbar';
import Footer from './components/Footer';


function App() {
  
  const navbarHeight = "48px";
  const footerHeight = "48px";
  
  return (
    <div className="bg-background min-h-screen">
      <BrowserRouter className="flex h-full w-full justify-center items-center"> 
        <Navbar height={navbarHeight}/>
        <Routes>
          <Route path="/" element={<HomePage navbarHeight={navbarHeight} footerHeight={footerHeight}/>} />
          <Route path="/chat" element={<ChatPage navbarHeight={navbarHeight} footerHeight={footerHeight}/>} />
        </Routes>
        <Footer height={footerHeight}/>
      </BrowserRouter>
    </div>
  );
}

export default App;


