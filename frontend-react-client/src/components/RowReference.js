import { Collapse } from '@material-ui/core';
import React, { useState } from 'react';
import interpolateHexColors from './utils';

const RowReference = ({ ...props }) => {
  const [expanded, setExpanded] = useState(false);

  const rowNo = parseInt(props.rowno, 10);
  const rowText = props.rowtext;
  const rowScore = parseFloat(props.rowscore);
  const rowContext = props.rowcontext;

  const hexGreen = "#00FF00";
  const hexRed = "#FF0000";
  const color = `${interpolateHexColors(hexRed, hexGreen, rowScore)}`;

  // Split rowContext into an array using #DELIMITER# as the separator
  const contextArray = rowContext.split('#DELIMITER#');

  const handleExpandClick = () => {
    setExpanded(!expanded);
  };

  // Build rows beforehand
  const rows = [
    // { number: rowNo - 1, text: contextArray[0], score: null },
    { number: rowNo, text: rowText, score: rowScore },
    // { number: rowNo + 1, text: contextArray[1], score: null },
  ];

  return (
    <span>
      <button onClick={handleExpandClick} style={{"color": color}}>
        <sup>{expanded ? `[#${rowNo}] Collapse` : `[#${rowNo}] Expand`}</sup>
      </button>
      <Collapse in={expanded} timeout="auto" unmountOnExit>
        <div className="m-2">
          <table className="w-full border-collapse border border-borderColor rounded-lg overflow-hidden">
            <thead>
              <tr className="bg-gray-200">
                <th className="border p-0.5">Row</th>
                <th className="border p-0.5">Log Message</th>
                <th className="border p-0.5">Retrieval Score</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((row, index) => (
                <tr key={index} className={index % 2 === 0 ? 'bg-gray-100 hover:bg-gray-300' : 'bg-white hover:bg-gray-300'}>
                  <td className="border p-0.5 text-center">{row.number}</td>
                  <td className="border p-0.5">{row.text}</td>
                  <td className="border p-0.5 text-center" style={{color: color}}>{row.score}</td>
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
