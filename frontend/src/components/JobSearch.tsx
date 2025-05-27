import React, { useState } from "react";
import { JobSearchParams } from "../types/job";

interface JobSearchProps {
  onSearch: (params: JobSearchParams) => void;
  isLoading: boolean;
}

const JobSearch: React.FC<JobSearchProps> = ({ onSearch, isLoading }) => {
  const [query, setQuery] = useState("");
  const [location, setLocation] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch({
      query,
      location,
      page: 1,
      limit: 10,
    });
  };

  return (
    <div className="w-full bg-white">
      <div className="w-full max-w-[2000px] mx-auto px-4 sm:px-6 lg:px-8 py-12 lg:py-16">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Find Your Dream Job
          </h1>
          <p className="text-lg text-gray-600 max-w-3xl mx-auto">
            Browse thousands of job listings from top companies and find the
            perfect role for your skills and experience.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="w-full max-w-4xl mx-auto">
          <div className="flex flex-col sm:flex-row gap-3 sm:gap-0 bg-white rounded-lg shadow-lg border border-gray-200 p-1">
            <div className="flex-1">
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                  <svg
                    className="h-5 w-5 text-gray-400"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path
                      fillRule="evenodd"
                      d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"
                      clipRule="evenodd"
                    />
                  </svg>
                </div>
                <input
                  id="query"
                  type="text"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Job title, keywords, or company"
                  className="w-full pl-12 pr-4 py-4 text-base border-0 rounded-l-lg bg-white text-black caret-black focus:ring-0 focus:outline-none"
                />
              </div>
            </div>
            <div className="flex-1 border-l border-gray-200">
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                  <svg
                    className="h-5 w-5 text-gray-400"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path
                      fillRule="evenodd"
                      d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z"
                      clipRule="evenodd"
                    />
                  </svg>
                </div>
                <input
                  id="location"
                  type="text"
                  value={location}
                  onChange={(e) => setLocation(e.target.value)}
                  placeholder="Location"
                  className="w-full pl-12 pr-4 py-4 text-base border-0 rounded-l-lg bg-white text-black caret-black focus:ring-0 focus:outline-none"
                />
              </div>
            </div>
            <button
              type="submit"
              disabled={isLoading}
              className={`px-8 py-4 border-0 text-base font-medium rounded-r-lg text-white ${
                isLoading ? "bg-gray-400" : "bg-gray-900 hover:bg-gray-800"
              } transition-colors duration-150 ease-in-out`}
            >
              {isLoading ? (
                <>
                  <svg
                    className="animate-spin -ml-1 mr-2 h-5 w-5 text-white inline"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    ></circle>
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    ></path>
                  </svg>
                  Searching...
                </>
              ) : (
                "Search Jobs"
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default JobSearch;
