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
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      // Read the response as a blob
      const blob = await response.blob();
      // Create a local URL for the blob to be used as a source for the video
      const videoUrl = URL.createObjectURL(blob);
      setVideoSrc(videoUrl);
    } catch (error) {
      console.error('There was an error fetching the MP4 file:', error);
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
