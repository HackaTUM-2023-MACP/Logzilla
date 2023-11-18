import React, { useState, useRef } from 'react';
import CircularProgress from '@material-ui/core/CircularProgress';


const UploadBox = () => {
  const [isDragging, setIsDragging] = useState(false);
  const [filePath, setFilePath] = useState(null); // New state variable for file path
  const fileInputRef = useRef(null);

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

    const files = e.dataTransfer.files;

    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
      formData.append('file', files[i]);
    }

    // Upload files now
    try {
      const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        setFilePath(files[0].name); // Set the file path upon successful upload
        console.log('Files uploaded successfully');
      } else {
        console.log('Failed to upload files');
      }
    } catch (error) {
      console.log('Error occurred while uploading files:', error);
    }
  };

  const handleBoxClick = () => {
    fileInputRef.current.click();
  };

  const handleFileInputChange = async (e) => {
    const files = e.target.files;

    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
      formData.append('file', files[i]);
    }

    // Upload files now
    try {
      const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        setFilePath(files[0].name); // Set the file path upon successful upload
        console.log('Files uploaded successfully');
      } else {
        console.log('Failed to upload files');
      }
    } catch (error) {
      console.log('Error occurred while uploading files:', error);
    }
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
          {filePath ? (
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
