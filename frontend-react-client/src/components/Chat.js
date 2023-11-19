import React, { useState, useEffect, useContext } from 'react';
import Message from './Message'; // Make sure to provide the correct path to the Message component
import TopKLogContext from './TopKLogContext';

const TypingIndicator = () => {
  const [dots, setDots] = useState('.');

  useEffect(() => {
    const interval = setInterval(() => {
      setDots((prevDots) => (prevDots === '...' ? '.' : prevDots + '.'));
    }, 500);

    return () => clearInterval(interval);
  }, []);

  return <div className="text-gray-500 text-md italic mb-2" style={{backgroundColor: '#1e2128'}}>Logzilla Bot is typing{dots}</div>;
};

const ChatComponent = ({ className }) => {
  const { topKLogRefs, setTopKLogRefs, summary, setSummary, logFileName, setLogFileName } = useContext(TopKLogContext);
  const [userMessages, setUserMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [botMessages, setBotMessages] = useState([`Hello there! I am able to customize the summary of ${logFileName} if you tell me what you want to know!`]);
  const [loading, setLoading] = useState(false);

  const handleUserMessageSubmit = async () => {
    const newUserMessages = [...userMessages, inputMessage];
    setUserMessages(newUserMessages);
    setInputMessage('');

    try {
      setLoading(true);
      const response = await fetch('/api/response', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          userMessages: newUserMessages,
          botMessages: botMessages,
          summary: summary,
        }),
      });

      const data = await response.json();
      const newBotMessages = [...botMessages, data.botResponse];
      setBotMessages(newBotMessages);
      setTopKLogRefs(data.filteredRows);
      setSummary(data.summary);
    } catch (error) {
      console.error('Error sending user message:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleUserMessageSubmit();
    }
  };

  return (
    <div className={`relative max-w-md mx-auto p-4 bg-gray-100 rounded-md shadow-md ${className} chatboxComponent`}>
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
          <React.Fragment key={`user-${index}`}>
            <Message
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
          </React.Fragment>
        ))}
      </div>
      <div className='absolute bottom-14'>{loading && <TypingIndicator />}</div>
      <div className="flex">
        <input
          type="text"
          className="flex-grow p-2 pl-4 border rounded-l-md focus:outline-none font-mono"
          placeholder="Type a message..."
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          style={{ backgroundColor: '#282c34', border: 'none', color: 'white' }}
        />
        <button
          className="bg-blue-500 text-white p-2 px-4 rounded-r-md hover:bg-blue-700 font-mono"
          onClick={handleUserMessageSubmit}
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatComponent;
