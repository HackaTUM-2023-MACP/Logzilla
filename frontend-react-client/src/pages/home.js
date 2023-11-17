import React, { useState, useEffect } from 'react';
import logo from '../logo.svg';

const HomePage = () => {

  // Add state to the application to hold data.
  // The function returns two values, a getter and a setter for the new state.
  // Using a setter function is necessary because by invoking the setter React is 
  // able to trigger updates in the parts of the application that depend on this state. 
  const [currentTime, setCurrentTime] = useState(0);

  // Issue a request from the frontend to the backend upon rendering the component.
  useEffect(
    // First argument is the callback function. 
    () => {
      fetch('/api/time').then(res => res.json()).then(data => {
        setCurrentTime(data.time);
      });
    }, 
    // second argument to useEffect() is optional and can be set to the list of state 
    // variables on which this callback depends. 
    []
  );

  return (
    <div className='flex flex-col items-center justify-center'>
      <img src={logo} className="App-logo" alt="logo" />
      <p className='text-textColor'>
        Edit <code>src/App.js</code> and save to reload.
      </p>
      <a
        className="text-textColor-light hover:underline"
        href="https://reactjs.org"
        target="_blank"
        rel="noopener noreferrer"
      >
        Learn React
      </a>
      <p>The current time is {currentTime}.</p>
    </div>
  )
}

export default HomePage