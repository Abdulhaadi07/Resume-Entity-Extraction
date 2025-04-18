import React from 'react';
import { useLocation } from 'react-router-dom';

const ParsedResumePage = () => {
  const location = useLocation();
  const parsedResume = location.state?.parsedResume;

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-md">
      <h1 className="text-2xl font-bold mb-6">Parsed Resume</h1>
      <div className="bg-gray-50 p-4 rounded-lg">
        <pre className="whitespace-pre-wrap">
          {JSON.stringify(parsedResume, null, 2)}
        </pre>
      </div>
    </div>
  );
};

export default ParsedResumePage;
