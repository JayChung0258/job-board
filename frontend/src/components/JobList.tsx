import React from "react";
import JobCard from "./JobCard";
import Pagination from "./Pagination";
import { Job } from "../types/job";

interface JobListProps {
  jobs: Job[];
  loading: boolean;
  error: string | null;
  pagination: {
    total: number;
    page: number;
    limit: number;
    pages: number;
  };
  searchParams: Record<string, any>;
  onPageChange: (page: number) => void;
  onClearFilters: () => void;
}

const JobList: React.FC<JobListProps> = ({
  jobs,
  loading,
  error,
  pagination,
  searchParams,
  onPageChange,
  onClearFilters,
}) => {
  if (error) {
    return (
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
    );
  }

  return (
    <div className="bg-white shadow-sm rounded-xl overflow-hidden border border-gray-200">
      <div className="p-6">
        {loading ? (
          <div className="flex flex-col items-center justify-center py-16 sm:py-20">
            <div className="inline-block h-10 w-10 sm:h-12 sm:w-12 animate-spin rounded-full border-4 border-solid border-blue-600 border-r-transparent"></div>
            <p className="mt-4 text-base sm:text-lg font-medium text-gray-700">
              Loading jobs...
            </p>
          </div>
        ) : jobs.length > 0 ? (
          <div>
            {/* Results Summary */}
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
                {Math.min(pagination.page * pagination.limit, pagination.total)}{" "}
                of {pagination.total}
              </div>
            </div>

            {/* Job Cards */}
            <div className="space-y-4 sm:space-y-6">
              {jobs.map((job) => (
                <JobCard key={job.job_id} job={job} />
              ))}
            </div>

            {/* Pagination */}
            <Pagination
              currentPage={pagination.page}
              totalPages={pagination.pages}
              onPageChange={onPageChange}
            />
          </div>
        ) : (
          // Empty State
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
              onClick={onClearFilters}
              className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
            >
              Clear all filters
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default JobList;
