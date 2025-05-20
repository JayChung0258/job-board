import React from "react";
import { Routes, Route } from "react-router-dom";
import JobListingPage from "./pages/JobListingPage";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import "./App.css";

const App: React.FC = () => {
  return (
    <div className="flex flex-col min-h-screen bg-gray-50">
      <Navbar />
      <main className="flex-grow">
        <Routes>
          <Route path="/" element={<JobListingPage />} />
          <Route
            path="/categories"
            element={
              <div className="max-w-7xl mx-auto px-4 py-12">Coming Soon</div>
            }
          />
          <Route
            path="/companies"
            element={
              <div className="max-w-7xl mx-auto px-4 py-12">Coming Soon</div>
            }
          />
        </Routes>
      </main>
      <Footer />
    </div>
  );
};

export default App;
