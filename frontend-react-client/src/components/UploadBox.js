import React, { useState, useRef } from 'react';
import CircularProgress from '@material-ui/core/CircularProgress';

import "./UploadBox.css";

const UploadBox = () => {
  const [isDragging, setIsDragging] = useState(false);
  const [isWaiting, setIsWaiting] = useState(false);
  const [filePath, setFilePath] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [tags, setTags] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedButtons, setSelectedButtons] = useState([]);

  const fileInputRef = useRef(null);


  const toggleTagSelection = (tag) => {
    setSelectedButtons(prevSelected => {
      if (prevSelected.includes(tag)) {
        return prevSelected.filter(t => t !== tag);
      } else {
        return [...prevSelected, tag];
      }
    });
  };

  const createFormData = (file) => {
    const formData = new FormData();
    formData.append('file', file ? file : selectedFile);
    formData.append('whitelist', selectedButtons);
    return formData;
  };

  const uploadFile = async (e) => {
    if (!selectedFile) {
      console.log('No file selected');
      return;
    }
    try {
      setIsWaiting(true);
      const formData = createFormData();
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

  const getTags = async (e) => {
    const files = e.dataTransfer.files;
    if (!files.length) return;
    const file = files[0];
    try {
      setIsWaiting(true);
      setSelectedFile(file);
      setFilePath(file.name);
      const formData = createFormData(file);

      const response = await fetch('/api/layers', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        console.log('File uploaded successfully (layers)');
        const data = await response.json(); 
        console.log(data);
        setTags(data.layers);

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
    if (isWaiting) return;
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
    if (isWaiting) return;
    e.preventDefault();
    setIsDragging(false);
    await getTags(e);
  };

  const handleBoxClick = () => {
    if (isWaiting) return;
    fileInputRef.current.click();
  };

  const handleFileInputChange = async (e) => {
    if (isWaiting) return;
    await getTags(e);
  };

  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value);
  };

  const filteredTags = tags.filter(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()));


  return (
    <div className='w-full h-full p-14'>
      <div
        className={`cursor-pointer flex items-center justify-center w-full h-full p-10 rounded-3xl ${
          isDragging ? 'border-2 border-dashed border-blue-500' : 'border-2 border-dashed border-gray-300'
        }`}
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        onClick={tags.length === 0 ? handleBoxClick : () => {}}
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
            <>
            <p hidden={tags.length > 0} className="text-4xl font-bold pointer-events-none">Drag and Drop Files to Upload</p>
            <div hidden={tags.length == 0}>
              <p className="text-4xl font-bold"  style={{"marginBottom": "1em"}}>What would you like to focus on?</p>
              {/* Search here that filters tags */}
              <input
                type="text"
                placeholder="Search tags..."
                value={searchTerm}
                onChange={handleSearchChange}
                className="mb-10 p-2 border rounded w-80"
              />
              <div style={{"height": "600px"}} className='masked-container'>
                {filteredTags.map((tag) => (
                  <button
                    className={`tagButton cursor-pointer bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full mr-5 mb-5 ${selectedButtons.includes(tag) ? 'selectedTag' : ''}`}
                    key={tag}
                    onClick={() => toggleTagSelection(tag)}
                  >
                  {tag}
                  </button>
                ))}
              </div>
              <button
                className="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full mt-10"
                onClick={uploadFile}
              >
                Continue
              </button>
            </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default UploadBox;
