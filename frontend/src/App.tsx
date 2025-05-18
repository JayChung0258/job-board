import React from "react";
import { Routes, Route } from "react-router-dom";
import JobListingPage from "./pages/JobListingPage";
import "./App.css";

const App: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <Routes>
        <Route path="/" element={<JobListingPage />} />
      </Routes>
    </div>
  );
};

export default App;
