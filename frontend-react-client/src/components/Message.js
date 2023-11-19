import React from 'react';

const Message = ({ isSent, message, senderName, profilePicture }) => {
  // Determine the alignment based on whether the message is sent or received
  const alignmentClass = isSent ? 'self-end' : 'self-start';

  return (
    <div className={`flex ${alignmentClass} mb-4 items-center`}>
      {/* Profile Picture */}
      {/* <img
        src={profilePicture}
        alt={`${senderName}'s profile`}
        className="w-8 h-8 rounded-full mr-2"
      /> */}

      {/* Message Container */}
      <div
        className={`bg-blue-500 text-white p-2 rounded-md max-w-xs break-words ${
          isSent ? 'ml-auto' : 'mr-auto'
        }`}
      >
        {/* Sender Name */}
        <p className="text-sm font-semibold">{senderName}</p>

        {/* Message Text */}
        <p className="text-md">{message}</p>
      </div>
    </div>
  );
};

export default Message;
