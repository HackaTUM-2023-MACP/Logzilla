import React, { useState, useEffect, useContext } from 'react';
import Markdown from 'react-markdown';
import RowReference from './RowReference';
import rehypeRaw from 'rehype-raw'
import TopKLogContext from './TopKLogContext';



const SummaryBox = ({ className }) => {
  const { topKLogRefs, setTopKLogRefs, summary, setSummary } = useContext(TopKLogContext);

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
  }, []);

  return (
    <div className={`w-max-full p-5 text-lg overflow-scroll bg-slate-50 ${className}`}>
      <Markdown
        children={summary}
        className={''}
        components={{
          // MUST NOT be camelCase
          myref: ({ node, ...props }) => <RowReference {...props} />,
        }}
        rehypePlugins={[rehypeRaw]}
      />
    </div>
  );
};

export default SummaryBox;
