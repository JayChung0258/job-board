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
    <div className="bg-white rounded-lg shadow-md p-6 mb-6">
      <h2 className="text-xl font-bold text-gray-800 mb-4">
        Find Your Next Job
      </h2>

      <form onSubmit={handleSubmit}>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div>
            <label
              htmlFor="query"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Search
            </label>
            <input
              id="query"
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Job title, company, or keyword"
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label
              htmlFor="location"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Location
            </label>
            <input
              id="location"
              type="text"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              placeholder="City, state, or 'Remote'"
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>

        {tagCategories.length > 0 && (
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Filter by tags
            </label>

            <div className="flex border-b border-gray-200 mb-3">
              {tagCategories.map((category) => (
                <button
                  key={category}
                  type="button"
                  onClick={() => setActiveCategory(category)}
                  className={`mr-4 py-2 text-sm font-medium transition-colors ${
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
              <div className="flex flex-wrap gap-2">
                {availableTags[activeCategory].map((tag) => (
                  <button
                    key={tag}
                    type="button"
                    onClick={() => handleTagToggle(tag)}
                    className={`text-sm px-3 py-1 rounded-full transition-colors ${
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
        )}

        <div className="flex justify-end">
          <button
            type="submit"
            disabled={isLoading}
            className={`px-6 py-2 rounded-md text-white font-medium ${
              isLoading ? "bg-blue-400" : "bg-blue-600 hover:bg-blue-700"
            } transition-colors`}
          >
            {isLoading ? "Searching..." : "Search Jobs"}
          </button>
        </div>
      </form>
    </div>
  );
};

export default JobSearch;
