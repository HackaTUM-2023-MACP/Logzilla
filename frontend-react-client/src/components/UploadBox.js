import React, { useState, useRef } from 'react';
import CircularProgress from '@material-ui/core/CircularProgress';

const UploadBox = () => {
  const [isDragging, setIsDragging] = useState(false);
  const [isWaiting, setIsWaiting] = useState(false);
  const [filePath, setFilePath] = useState(null); // New state variable for file path
  const fileInputRef = useRef(null);

  const uploadFile = async (e) => {
    const files = e.dataTransfer.files;
    if (!files.length) return;
    const file = files[0];
    try {
      setIsWaiting(true);
      setFilePath(file.name);
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        console.log('File uploaded successfully');
        // TODO: Router
        window.location.href = '/chat';
      } else {
        console.log('Failed to upload file');
      }
      setIsWaiting(false);
    }

    catch (error) {
      console.log('Error occurred while uploading file:', error);
    }


  };

  const handleDragEnter = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = async (e) => {
    e.preventDefault();
    setIsDragging(false);
    await uploadFile(e);
  };

  const handleBoxClick = () => {
    fileInputRef.current.click();
  };

  const handleFileInputChange = async (e) => {
    await uploadFile(e);
  };

  return (
    <div className='w-full h-full p-14'>
      <div
        className={`flex items-center justify-center w-full h-full p-10 rounded-3xl ${
          isDragging ? 'border-2 border-dashed border-blue-500' : 'border-2 border-dashed border-gray-300'
        }`}
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        onClick={handleBoxClick}
      >
        <input
          type="file"
          ref={fileInputRef}
          style={{ display: 'none' }}
          onChange={handleFileInputChange}
        />
        <div className="text-center">
          {isWaiting ? (
            <div>
              <p className="text-4xl font-bold mb-10">{filePath}</p>
              <p className='mb-5'>Processing</p>
              <CircularProgress/>
            </div>
          ) : (
            <p className="text-4xl font-bold">Drag and Drop Files to Upload</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default UploadBox;
