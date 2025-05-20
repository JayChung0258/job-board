import React, { useState, useEffect } from "react";
import { searchJobs } from "../api/jobsApi";
import { Job, JobSearchParams, JobSearchResponse } from "../types/job";
import JobSearch from "../components/JobSearch";
import JobCard from "../components/JobCard";
import Pagination from "../components/Pagination";

const JobListingPage: React.FC = () => {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
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

  const handleSearch = async (params: JobSearchParams) => {
    setSearchParams(params);
    await fetchJobs(params);
  };

  const handlePageChange = (page: number) => {
    const newParams = { ...searchParams, page };
    setSearchParams(newParams);
    fetchJobs(newParams);
    // Scroll to top when changing pages
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

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

  useEffect(() => {
    fetchJobs(searchParams);
  }, []);

  return (
    <div className="w-full bg-gray-50">
      <div className="w-full max-w-[2000px] mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-10">
        <div className="mb-8 sm:mb-10">
          <h1 className="text-3xl sm:text-4xl font-extrabold text-gray-900 tracking-tight mb-2 sm:mb-4">
            Find Your Next Tech Job
          </h1>
          <p className="text-lg sm:text-xl text-gray-600 max-w-3xl">
            Browse through hundreds of tech opportunities from top companies
          </p>
        </div>

        <div className="mb-8 sm:mb-10">
          <JobSearch onSearch={handleSearch} isLoading={loading} />
        </div>

        {error && (
          <div className="mb-8 rounded-lg bg-red-50 p-4 border-l-4 border-red-500">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg
                  className="h-5 w-5 text-red-400"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                    clipRule="evenodd"
                  />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-red-700">{error}</p>
              </div>
            </div>
          </div>
        )}

        <div className="bg-white shadow-sm rounded-xl overflow-hidden border border-gray-200">
          <div className="p-4 sm:p-6">
            {loading ? (
              <div className="flex flex-col items-center justify-center py-16 sm:py-20">
                <div className="inline-block h-10 w-10 sm:h-12 sm:w-12 animate-spin rounded-full border-4 border-solid border-blue-600 border-r-transparent"></div>
                <p className="mt-4 text-base sm:text-lg font-medium text-gray-700">
                  Loading jobs...
                </p>
              </div>
            ) : jobs.length > 0 ? (
              <div>
                <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center mb-6 pb-4 border-b border-gray-200 gap-2">
                  <div className="text-gray-700">
                    <span className="font-medium">{pagination.total}</span> jobs
                    found
                    {Object.keys(searchParams).length > 2 && (
                      <span className="ml-1">based on your search</span>
                    )}
                  </div>
                  <div className="text-sm text-gray-500">
                    Showing {(pagination.page - 1) * pagination.limit + 1}-
                    {Math.min(
                      pagination.page * pagination.limit,
                      pagination.total,
                    )}{" "}
                    of {pagination.total}
                  </div>
                </div>

                <div className="space-y-4 sm:space-y-6">
                  {jobs.map((job) => (
                    <JobCard key={job.job_id} job={job} />
                  ))}
                </div>

                <Pagination
                  currentPage={pagination.page}
                  totalPages={pagination.pages}
                  onPageChange={handlePageChange}
                />
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center py-16 sm:py-20 text-center">
                <svg
                  className="h-12 w-12 sm:h-16 sm:w-16 text-gray-400 mb-4"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="1.5"
                    d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
                <h3 className="text-lg font-medium text-gray-900 mb-1">
                  No jobs found
                </h3>
                <p className="text-gray-600 max-w-md mb-4">
                  We couldn't find any jobs matching your search criteria. Try
                  adjusting your filters or search terms.
                </p>
                <button
                  onClick={() => handleSearch({ page: 1, limit: 10 })}
                  className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                >
                  Clear all filters
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default JobListingPage;
