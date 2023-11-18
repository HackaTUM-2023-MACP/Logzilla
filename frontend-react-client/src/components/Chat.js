import React, { useState, useEffect } from 'react';
import Message from './Message'; // Make sure to provide the correct path to the Message component

const ChatComponent = ({ className }) => {
  const [userMessages, setUserMessages] = useState([]);
  const [botMessages, setBotMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');

  useEffect(() => {
    // Fetch initial messages from the server
    fetchMessages();
  }, []);

  const fetchMessages = async () => {
    try {
      const response = await fetch('/api/chat-messages');
      const data = await response.json();
      const { userMessages, botMessages } = data;
      setUserMessages(userMessages);
      setBotMessages(botMessages);
    } catch (error) {
      console.error('Error fetching messages:', error);
    }
  };

  const handleUserMessageSubmit = async () => {
    // Simulate sending a user message and getting a bot response
    const newUserMessages = [...userMessages, inputMessage];
    setUserMessages(newUserMessages);
    setInputMessage('');

    try {
      const response = await fetch('/api/response', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          userMessages: userMessages,
          botMessages: botMessages
        }),
      });

      const data = await response.json();
      const lastBotMessage = data.botMessages[data.botMessages.length - 1];
      const newBotMessages = [...botMessages, lastBotMessage];
      setBotMessages(newBotMessages);
    } catch (error) {
      console.error('Error sending user message:', error);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleUserMessageSubmit();
    }
  };

  return (
    <div className={`max-w-md mx-auto p-4 bg-gray-100 rounded-md shadow-md ${className}`}>
      <div className="h-64 overflow-y-auto mb-4">
        {userMessages.map((message, index) => (
          <Message
            key={`user-${index}`}
            isSent={true}
            message={message}
            senderName="You"
            profilePicture="your_profile_picture_url"
          />
        ))}
        {botMessages.map((message, index) => (
          <Message
            key={`bot-${index}`}
            isSent={false}
            message={message}
            senderName="Bot"
            profilePicture="bot_profile_picture_url"
          />
        ))}
      </div>
      <div className="flex">
        <input
          type="text"
          className="flex-grow p-2 border rounded-l-md focus:outline-none"
          placeholder="Type a message..."
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyPress={handleKeyPress} // Add event listener for key press
        />
        <button
          className="bg-blue-500 text-white p-2 rounded-r-md hover:bg-blue-700"
          onClick={handleUserMessageSubmit}
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatComponent;
