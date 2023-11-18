import React, { useState } from 'react';

const VideoComponent = () => {
  const [selectedOption, setSelectedOption] = useState('');
  const [videoSrc, setVideoSrc] = useState('');

  const handleRunClick = async () => {
    try {
      const response = await fetch('/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ option: selectedOption }),
      });
      const data = await response.json();
      setVideoSrc(data.mp4Url);
    } catch (error) {
      console.error('There was an error fetching the MP4 file:', error);
      // Just temporary until we have proper video logic on backend
      setVideoSrc(`${process.env.PUBLIC_URL}/test.mp4`)
    }
  };

  return (
    <div>
      <select onChange={e => setSelectedOption(e.target.value)} value={selectedOption}>
        <option value="">Select Option</option>
        <option value="option1">Option 1</option>
        {/* Add more options here as needed */}
      </select>
      <button onClick={handleRunClick} disabled={!selectedOption}>Run</button>
      {videoSrc && <video controls src={videoSrc} />}
    </div>
  );
};

export default VideoComponent;
