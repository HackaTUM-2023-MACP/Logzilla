import { Collapse } from '@material-ui/core';
import React, { useState } from 'react';

const RowReference = ({ ...props }) => {
  const [expanded, setExpanded] = useState(false);

  const rowNo = parseInt(props.rowno, 10);
  const rowText = props.rowtext;
  const rowScore = parseFloat(props.rowscore);
  const rowContext = props.rowcontext;

  // Split rowContext into an array using #DELIMITER# as the separator
  const contextArray = rowContext.split('#DELIMITER#');

  const handleExpandClick = () => {
    setExpanded(!expanded);
  };

  // Build rows beforehand
  const rows = [
    { number: rowNo - 1, text: contextArray[0], score: null },
    { number: rowNo, text: rowText, score: rowScore },
    { number: rowNo + 1, text: contextArray[1], score: null },
  ];

  return (
    <span>
      <button onClick={handleExpandClick} className='text-primary'>
        <sup>{expanded ? `[#${rowNo}] Collapse` : `[#${rowNo}] Expand`}</sup>
      </button>
      <Collapse in={expanded} timeout="auto" unmountOnExit>
        <div className="mt-4">
          <table className="w-full border-collapse border">
            <thead>
              <tr className="bg-gray-200">
                <th className="border p-2">Row</th>
                <th className="border p-2">Log Message</th>
                <th className="border p-2">Retrieval Score</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((row, index) => (
                <tr key={index}>
                  <td className="border p-2">{row.number}</td>
                  <td className="border p-2">{row.text}</td>
                  <td className="border p-2">{row.score}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Collapse>
    </span>
  );
};

export default RowReference;
