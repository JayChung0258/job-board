import React, { useState, useEffect } from "react";
import { JobSearchParams } from "../types/job";
import { getTagCategories, getTagsByCategory } from "../api/jobsApi";

interface JobSearchProps {
  onSearch: (params: JobSearchParams) => void;
  isLoading: boolean;
}

const JobSearch: React.FC<JobSearchProps> = ({ onSearch, isLoading }) => {
  const [query, setQuery] = useState("");
  const [location, setLocation] = useState("");
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [availableTags, setAvailableTags] = useState<Record<string, string[]>>(
    {},
  );
  const [tagCategories, setTagCategories] = useState<string[]>([]);
  const [activeCategory, setActiveCategory] = useState<string>("");
  const [isAdvancedSearchOpen, setIsAdvancedSearchOpen] = useState(false);

  useEffect(() => {
    // Load tag categories when component mounts
    const loadTagCategories = async () => {
      try {
        const categories = await getTagCategories();
        setTagCategories(categories);
        if (categories.length > 0) {
          setActiveCategory(categories[0]);
        }
      } catch (error) {
        console.error("Failed to load tag categories:", error);
      }
    };

    loadTagCategories();
  }, []);

  useEffect(() => {
    // Load tags for active category
    if (activeCategory) {
      const loadTags = async () => {
        try {
          const tags = await getTagsByCategory(activeCategory);
          setAvailableTags((prevTags) => ({
            ...prevTags,
            [activeCategory]: tags,
          }));
        } catch (error) {
          console.error(`Failed to load tags for ${activeCategory}:`, error);
        }
      };

      if (!availableTags[activeCategory]) {
        loadTags();
      }
    }
  }, [activeCategory, availableTags]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch({
      query,
      location,
      tags: selectedTags.length > 0 ? selectedTags : undefined,
      page: 1,
      limit: 10,
    });
  };

  const handleTagToggle = (tag: string) => {
    if (selectedTags.includes(tag)) {
      setSelectedTags(selectedTags.filter((t) => t !== tag));
    } else {
      setSelectedTags([...selectedTags, tag]);
    }
  };

  return (
    <div className="bg-gradient-to-r from-blue-600 to-blue-800 rounded-xl shadow-xl overflow-hidden">
      <div className="px-6 py-8 md:px-10 md:py-12">
        <h2 className="text-2xl md:text-3xl font-bold text-white mb-2">
          Find Your Dream Job
        </h2>
        <p className="text-blue-100 mb-8">
          Search through thousands of jobs from top companies
        </p>

        <form onSubmit={handleSubmit}>
          <div className="flex flex-col md:flex-row gap-4 mb-6">
            <div className="flex-1">
              <div className="relative rounded-md shadow-sm">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
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
                  placeholder="Job title, company, or keyword"
                  className="focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 pr-3 py-3 text-base border-gray-300 rounded-md"
                />
              </div>
            </div>
            <div className="flex-1">
              <div className="relative rounded-md shadow-sm">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
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
                  placeholder="City, state, or 'Remote'"
                  className="focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 pr-3 py-3 text-base border-gray-300 rounded-md"
                />
              </div>
            </div>
            <button
              type="submit"
              disabled={isLoading}
              className={`inline-flex items-center justify-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white ${
                isLoading ? "bg-blue-400" : "bg-blue-900 hover:bg-blue-950"
              } transition-colors duration-150 ease-in-out`}
            >
              {isLoading ? (
                <>
                  <svg
                    className="animate-spin -ml-1 mr-2 h-5 w-5 text-white"
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
                <>
                  <svg
                    className="mr-2 h-5 w-5"
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
                  Search Jobs
                </>
              )}
            </button>
          </div>

          <div className="flex justify-center mb-2">
            <button
              type="button"
              onClick={() => setIsAdvancedSearchOpen(!isAdvancedSearchOpen)}
              className="text-blue-100 hover:text-white text-sm flex items-center focus:outline-none transition-colors duration-150 ease-in-out"
            >
              {isAdvancedSearchOpen ? (
                <>
                  <svg
                    className="mr-1 h-4 w-4"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path
                      fillRule="evenodd"
                      d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z"
                      clipRule="evenodd"
                    />
                  </svg>
                  Hide advanced filters
                </>
              ) : (
                <>
                  <svg
                    className="mr-1 h-4 w-4"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path
                      fillRule="evenodd"
                      d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                      clipRule="evenodd"
                    />
                  </svg>
                  Show advanced filters
                </>
              )}
            </button>
          </div>

          {isAdvancedSearchOpen && tagCategories.length > 0 && (
            <div className="bg-white rounded-lg p-4 mt-4 shadow-inner">
              <div className="mb-4">
                <p className="text-sm font-medium text-gray-700 mb-2">
                  Filter by tags:
                </p>

                <div className="flex flex-wrap border-b border-gray-200 mb-3 gap-x-4">
                  {tagCategories.map((category) => (
                    <button
                      key={category}
                      type="button"
                      onClick={() => setActiveCategory(category)}
                      className={`py-2 text-sm font-medium transition-colors ${
                        activeCategory === category
                          ? "text-blue-600 border-b-2 border-blue-600"
                          : "text-gray-500 hover:text-gray-700"
                      }`}
                    >
                      {category.charAt(0).toUpperCase() + category.slice(1)}
                    </button>
                  ))}
                </div>

                {activeCategory && availableTags[activeCategory] && (
                  <div className="flex flex-wrap gap-2 mt-3">
                    {availableTags[activeCategory].map((tag) => (
                      <button
                        key={tag}
                        type="button"
                        onClick={() => handleTagToggle(tag)}
                        className={`text-sm px-3 py-1.5 rounded-full transition-colors ${
                          selectedTags.includes(tag)
                            ? "bg-blue-600 text-white"
                            : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                        }`}
                      >
                        {tag.replace(/-/g, " ")}
                      </button>
                    ))}
                  </div>
                )}
              </div>

              {selectedTags.length > 0 && (
                <div className="mt-4">
                  <div className="flex items-center justify-between">
                    <p className="text-sm font-medium text-gray-700">
                      Selected filters:
                    </p>
                    <button
                      type="button"
                      onClick={() => setSelectedTags([])}
                      className="text-xs text-blue-600 hover:text-blue-800"
                    >
                      Clear all
                    </button>
                  </div>
                  <div className="flex flex-wrap gap-2 mt-2">
                    {selectedTags.map((tag) => (
                      <span
                        key={tag}
                        className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                      >
                        {tag.replace(/-/g, " ")}
                        <button
                          type="button"
                          onClick={() => handleTagToggle(tag)}
                          className="flex-shrink-0 ml-1 h-4 w-4 rounded-full inline-flex items-center justify-center text-blue-600 hover:text-blue-800 focus:outline-none"
                        >
                          <span className="sr-only">Remove filter</span>
                          <svg
                            className="h-2 w-2"
                            stroke="currentColor"
                            fill="none"
                            viewBox="0 0 8 8"
                          >
                            <path
                              strokeLinecap="round"
                              strokeWidth="1.5"
                              d="M1 1l6 6m0-6L1 7"
                            />
                          </svg>
                        </button>
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </form>
      </div>
    </div>
  );
};

export default JobSearch;
