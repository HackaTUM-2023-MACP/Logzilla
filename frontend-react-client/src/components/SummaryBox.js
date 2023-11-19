import React, { useState, useEffect, useContext } from 'react';
import Markdown from 'react-markdown';
import RowReference from './RowReference';
import rehypeRaw from 'rehype-raw';
import CircularProgress from '@material-ui/core/CircularProgress';
import TopKLogContext from './TopKLogContext';

const SummaryBox = ({ className }) => {
  const { topKLogRefs, summary, setSummary } = useContext(TopKLogContext);
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
    <div className={`relative w-max-full p-5 text-lg overflow-scroll bg-slate-50 ${className} minheight`}>
      {loading && (
        <div className="absolute top-0 left-0 right-0 bottom-0 flex justify-center items-center bg-slate-50 bg-opacity-50 z-10">
          <CircularProgress />
        </div>
      )}
      <Markdown
        children={summary}
        className={''}
        components={{
          myref: ({ node, ...props }) => <RowReference {...props} />,
        }}
        rehypePlugins={[rehypeRaw]}
      />
    </div>
  );
};

export default SummaryBox;
