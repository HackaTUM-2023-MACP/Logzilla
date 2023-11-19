import React, { useState, useEffect, useContext } from 'react';
import Markdown from 'react-markdown';
import RowReference from './RowReference';
import rehypeRaw from 'rehype-raw';
import CircularProgress from '@material-ui/core/CircularProgress';
import TopKLogContext from './TopKLogContext';
import interpolateHexColors from './utils';

const SummaryBox = ({ className }) => {
  const { topKLogRefs, setTopKLogRefs, summary, setSummary } = useContext(TopKLogContext);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true); // Start loading
    fetch('/api/summary', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ currentSummary: summary, topKLogRefs }),
    })
      .then(response => response.json())
      .then(data => {
        setSummary(data.updatedSummary.trim());
        setLoading(false); // Stop loading once data is received
      })
      .catch(error => {
        console.error('Error fetching summary:', error);
        setLoading(false); // Stop loading if there's an error
      });
  }, []); // Removed dependencies to only fetch on mount

  return (
    <div className={`relative w-max-full p-5 text-lg rounded-md shadow-md overflow-scroll bg-slate-50 ${className} summaryboxComponent`}>
      {loading && (
        <div className="absolute top-0 left-0 right-0 bottom-0 flex justify-center items-center z-10">
          <CircularProgress />
        </div>
      )}
      <div>
        <p className='font-bold mb-3 text-lg font-mono'>Summary</p>
        <Markdown
          children={summary}
          className={''}
          components={{
            myref: ({ node, ...props }) => <RowReference {...props} />,
          }}
          rehypePlugins={[rehypeRaw]}
        />
        <p className='font-bold mb-3 mt-5 text-lg font-mono'>Relevant Rows</p>
        <div className="m-2">
          <table className="w-full border-collapse border border-borderColor rounded-lg overflow-hidden">
            <thead>
              <tr className="rowReferenceHeader">
                <th className="border p-0.5">Row</th>
                <th className="border p-0.5">Log Message</th>
                <th className="border p-0.5">Retrieval Score</th>
              </tr>
            </thead>
            { topKLogRefs !== undefined ? <tbody>
              {topKLogRefs.map((row, index) => (
                <tr key={index} className={index % 2 === 0 ? 'rowReferenceBodyEven' : 'rowReferenceBodyOdd'}>
                  <td className="border p-0.5 text-center">{row.rowNo}</td>
                  <td className="border p-0.5">{row.msg}</td>
                  <td className="border p-0.5 text-center" style={{color: interpolateHexColors("#FF0000", "#00FF00", row.score)}}>{row.score}</td>
                </tr>
              ))}
            </tbody> : null }
          </table>
        </div>
      </div>
    </div>
  );
};

export default SummaryBox;
