import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ResumeParser from './ResumeParser';
import ParsedResumePage from './ParsedResumePage';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<ResumeParser />} />
        <Route path="/parsed" element={<ParsedResumePage />} />
      </Routes>
    </Router>
  );
};

export default App;
