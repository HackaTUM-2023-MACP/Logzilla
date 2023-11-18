import React from 'react'
import Markdown from 'react-markdown'
import LogReference from './LogReference'


const SummaryBox = ({markdown, className}) => {

  return (
    <div className={`w-full h-full bg-slate-50 ${className}`}>
      <Markdown
        children={markdown}
        components={{
          logRef: ({ rowNo, rowText }) => <LogReference rowNo={rowNo} rowText={rowText} />,
        }}
      />
    </div>
  )
}

export default SummaryBox