import React, { useState, useEffect } from "react";
import { searchJobs } from "../api/jobsApi";
import { Job, JobSearchParams, JobSearchResponse } from "../types/job";
import JobSearch from "../components/JobSearch";
import JobList from "../components/JobList";
import JobFilter, { FilterState } from "../components/JobFilter";

/**
 * JobListingPage Component
 *
 * Main page component for job search and filtering coordination.
 * Acts as a container component that manages state and coordinates between
 * search, filter, and listing components.
 *
 * Features:
 * - Coordinates job search with query and location
 * - Manages filter state and application
 * - Handles pagination and state management
 * - Provides clean separation of concerns
 */
const JobListingPage: React.FC = () => {
  // Core data state
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Search and pagination state
  const [searchParams, setSearchParams] = useState<JobSearchParams>({
    page: 1,
    limit: 10,
  });
  const [pagination, setPagination] = useState({
    total: 0,
    page: 1,
    limit: 10,
    pages: 0,
  });

  // Filter state
  const [activeFilters, setActiveFilters] = useState<FilterState>({
    selectedTags: {},
    salaryRange: [50, 150],
    salaryFilterActive: false,
  });

  /**
   * Handles search form submission
   * @param params - Search parameters including query, location, pagination
   */
  const handleSearch = async (params: JobSearchParams) => {
    setSearchParams(params);
    await fetchJobs(params);
  };

  /**
   * Converts filter state to API search parameters and applies them
   * @param filters - Current filter state from JobFilter component
   */
  const handleFilterApply = (filters: FilterState) => {
    setActiveFilters(filters);

    // Convert filters to search params
    const selectedTagsArray: string[] = [];
    const selectedCategories: string[] = [];

    // Extract all selected tags and their categories
    Object.entries(filters.selectedTags).forEach(([category, tags]) => {
      if (tags.length > 0) {
        selectedTagsArray.push(...tags);
        if (!selectedCategories.includes(category)) {
          selectedCategories.push(category);
        }
      }
    });

    const newParams: JobSearchParams = {
      ...searchParams,
      page: 1, // Reset to first page when applying filters
    };

    // Add tag filters if any tags are selected
    if (selectedTagsArray.length > 0) {
      newParams.tags = selectedTagsArray;
    }

    if (selectedCategories.length > 0) {
      newParams.tag_categories = selectedCategories;
    }

    // Add salary filtering if active
    if (filters.salaryFilterActive) {
      // Convert salary range from thousands to actual values (50k → 50000)
      newParams.salary_min = filters.salaryRange[0] * 1000;
      newParams.salary_max = filters.salaryRange[1] * 1000;
    }

    console.log("Applying filters with params:", newParams);
    setSearchParams(newParams);
    fetchJobs(newParams);
  };

  /**
   * Resets all filters to default state while preserving search query
   */
  const handleFilterReset = () => {
    const resetFilters: FilterState = {
      selectedTags: {},
      salaryRange: [50, 150],
      salaryFilterActive: false,
    };
    setActiveFilters(resetFilters);

    // Reset search params to only include pagination, removing all filter params
    const newParams: JobSearchParams = {
      page: 1,
      limit: searchParams.limit || 10,
    };

    // Preserve search query if it exists
    if (searchParams.query) {
      newParams.query = searchParams.query;
    }
    if (searchParams.location) {
      newParams.location = searchParams.location;
    }

    console.log("Resetting filters with params:", newParams);
    setSearchParams(newParams);
    fetchJobs(newParams);
  };

  /**
   * Handles pagination changes and scrolls to top
   * @param page - Target page number
   */
  const handlePageChange = (page: number) => {
    const newParams = { ...searchParams, page };
    setSearchParams(newParams);
    fetchJobs(newParams);
    // Scroll to top when changing pages
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  /**
   * Handles clearing all filters from the empty state
   */
  const handleClearAllFilters = () => {
    handleFilterReset();
    handleSearch({ page: 1, limit: 10 });
  };

  /**
   * Fetches jobs from API with current search parameters
   * Handles loading states and error management
   * @param params - Search parameters to send to API
   */
  const fetchJobs = async (params: JobSearchParams) => {
    setLoading(true);
    setError(null);

    try {
      console.log("Fetching jobs with params:", params);
      const response: JobSearchResponse = await searchJobs(params);
      setJobs(response.items);
      setPagination({
        total: response.total,
        page: response.page,
        limit: response.limit,
        pages: response.pages,
      });
    } catch (err) {
      setError("Failed to fetch jobs. Please try again later.");
      console.error("Error fetching jobs:", err);
    } finally {
      setLoading(false);
    }
  };

  // Load initial jobs
  useEffect(() => {
    fetchJobs(searchParams);
  }, []);

  return (
    <div className="w-full bg-gray-50 min-h-screen">
      {/* Search Section - Full Width at Top */}
      <div className="w-full bg-white border-b border-gray-200">
        <JobSearch onSearch={handleSearch} isLoading={loading} />
      </div>

      {/* Main Content Area */}
      <div className="w-full max-w-[2000px] mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Filter Sidebar - Left Side */}
          <div className="w-full lg:w-80 flex-shrink-0">
            <div className="sticky top-8">
              <JobFilter
                onFilterApply={handleFilterApply}
                onFilterReset={handleFilterReset}
              />
            </div>
          </div>

          {/* Job Listings - Right Side */}
          <div className="flex-1 min-w-0">
            <JobList
              jobs={jobs}
              loading={loading}
              error={error}
              pagination={pagination}
              searchParams={searchParams}
              onPageChange={handlePageChange}
              onClearFilters={handleClearAllFilters}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default JobListingPage;
