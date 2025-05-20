import React from "react";
import { Routes, Route } from "react-router-dom";
import JobListingPage from "./pages/JobListingPage";
import CompaniesPage from "./pages/CompaniesPage";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import "./App.css";

const App: React.FC = () => {
  return (
    <div className="flex flex-col min-h-screen w-full">
      <Navbar />
      <main className="flex-grow w-full">
        <Routes>
          <Route path="/" element={<JobListingPage />} />
          <Route path="/companies" element={<CompaniesPage />} />
        </Routes>
      </main>
      <Footer />
    </div>
  );
};

export default App;
