import React, { useState, useEffect, useContext } from 'react';
import Message from './Message'; // Make sure to provide the correct path to the Message component
import TopKLogContext from './TopKLogContext';

const ChatComponent = ({ className }) => {
  const { topKLogRefs, setTopKLogRefs, summary, setSummary, logFileName, setLogFileName  } = useContext(TopKLogContext);
  const [userMessages, setUserMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [botMessages, setBotMessages] = useState([`Hello there! I am able to customize the summary of ${logFileName} if you tell me what you want to know!`]);

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
          userMessages: newUserMessages,
          botMessages: botMessages
        }),
      });

      const data = await response.json();
      const newBotMessages = [...botMessages, data.botResponse];
      setBotMessages(newBotMessages);
      setTopKLogRefs(data.filteredRows);
      setSummary(data.summary);
    } catch (error) {
      console.error('Error sending user message:', error);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleUserMessageSubmit();
    }
  };

  useEffect(() => {
    // Code to execute when botMessages changes
    // This will re-render the component whenever botMessages changes
  }, [botMessages]);

  return (
    <div className={`max-w-md mx-auto p-4 bg-gray-100 rounded-md shadow-md ${className} chatboxComponent`}>
      <div className="h-64 overflow-y-auto mb-4 chatboxContent">
        {botMessages.length > 0 && (
          <Message
            key={`bot-initial`}
            isSent={false}
            message={botMessages[0]}
            senderName="Logzilla Bot"
            profilePicture="bot_profile_picture_url"
          />
        )}
        {userMessages.map((message, index) => (
          <>
            <Message
              key={`user-${index}`}
              isSent={true}
              message={message}
              senderName="You"
              profilePicture="your_profile_picture_url"
            />
            {botMessages[index + 1] && (
              <Message
                key={`bot-${index}`}
                isSent={false}
                message={botMessages[index + 1]}
                senderName="Logzilla Bot"
                profilePicture="bot_profile_picture_url"
              />
            )}
          </>
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
          style={{ backgroundColor: '#282c34', border: 'none', color: 'white' }}
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
}

export default ChatComponent;
