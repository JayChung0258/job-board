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
  };

  const fetchJobs = async (params: JobSearchParams) => {
    setLoading(true);
    setError(null);

    try {
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
    <div className="max-w-7xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Job Board</h1>

      <JobSearch onSearch={handleSearch} isLoading={loading} />

      {error && (
        <div
          className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6"
          role="alert"
        >
          <p>{error}</p>
        </div>
      )}

      <div className="mb-6">
        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-blue-600 border-r-transparent"></div>
            <p className="mt-2 text-gray-600">Loading jobs...</p>
          </div>
        ) : jobs.length > 0 ? (
          <div>
            <div className="mb-4 text-gray-600">
              Showing {jobs.length} of {pagination.total} jobs
            </div>

            <div className="grid grid-cols-1 gap-6">
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
          <div className="text-center py-12">
            <p className="text-gray-600">
              No jobs found matching your criteria.
            </p>
            <p className="text-gray-500 mt-2">
              Try changing your search terms or filters.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default JobListingPage;
