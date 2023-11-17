import React from 'react';
import { BrowserRouter, Link, Routes, Route } from 'react-router-dom';
import './App.css';
import HomePage from './pages/home';
import Page2 from './pages/page2';
import Navbar from './components/navbar';

function App() {

  return (
    <div className="bg-background min-h-screen">
      <BrowserRouter className="flex h-full w-full"> 
        <Navbar/>
        <Routes>
          <Route path="/" Component={HomePage}/>
          <Route path="/page2" Component={Page2}/>
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;


