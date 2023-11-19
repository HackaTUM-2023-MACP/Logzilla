import React from 'react';
import GitHubIcon from '@mui/icons-material/GitHub';


const Footer = ({ height }) => {
  const currentYear = new Date().getFullYear();

  return (
    <footer 
      className='flex justify-between footerComponent'
      style={{ height: `${height}` }}
    >
      <div className="left">© {currentYear}</div>
      <div className="center">Made with 🥨 in Munich.</div>
      <div className="right">
        <a href="https://github.com/HackaTUM-2023-MACP/Logzilla/tree/main"><GitHubIcon className='scale-110'/></a>
      </div>
    </footer>
  );
};

export default Footer;
