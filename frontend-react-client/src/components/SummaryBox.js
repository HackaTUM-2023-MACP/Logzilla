import React, { useState, useEffect } from 'react';
import Markdown from 'react-markdown';
import RowReference from './RowReference';
import rehypeRaw from 'rehype-raw'


const SummaryBox = ({ className }) => {
  const [summary, setSummary] = useState('');
  const [topKLogRefs, setTopKLogRefs] = useState([]);

  useEffect(() => {
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
      })
      .catch(error => {
        console.error('Error fetching summary:', error);
      });
  }, [summary, topKLogRefs]);

  console.log('summary:', summary);

  return (
    <div className={`w-max-full h-full p-5 bg-slate-50 ${className}`}>
      <Markdown
        children={summary}
        className={'overflow-scroll'}
        components={{
          // MUST NOT be camelCase
          myref: ({ node, ...props }) => <RowReference {...props} />,
        }}
        rehypePlugins={[rehypeRaw]}
      />
    </div>
  );
};

export default SummaryBox