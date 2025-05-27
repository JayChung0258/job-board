import React from "react";

interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
}

/**
 * Modern Pagination Component
 *
 * Clean, accessible pagination with smooth transitions and clear visual hierarchy.
 * Features ellipsis for large page ranges and disabled states for navigation.
 */
const Pagination: React.FC<PaginationProps> = ({
  currentPage,
  totalPages,
  onPageChange,
}) => {
  if (totalPages <= 1) return null;

  const generatePageNumbers = () => {
    const pages = [];
    const maxVisiblePages = 7; // Increased for better UX

    if (totalPages <= maxVisiblePages) {
      // Show all pages if we have 7 or fewer
      for (let i = 1; i <= totalPages; i++) {
        pages.push(i);
      }
    } else {
      // Always show first page
      pages.push(1);

      // Calculate start and end for visible page numbers
      let startPage = Math.max(2, currentPage - 2);
      let endPage = Math.min(totalPages - 1, startPage + 3);

      // Adjust if we're too close to the end
      if (endPage === totalPages - 1) {
        startPage = Math.max(2, endPage - 3);
      }

      // Add ellipsis after first page if needed
      if (startPage > 2) {
        pages.push("ellipsis1");
      }

      // Add visible page numbers
      for (let i = startPage; i <= endPage; i++) {
        pages.push(i);
      }

      // Add ellipsis before last page if needed
      if (endPage < totalPages - 1) {
        pages.push("ellipsis2");
      }

      // Always show last page
      if (totalPages > 1) {
        pages.push(totalPages);
      }
    }

    return pages;
  };

  const handlePrevious = () => {
    if (currentPage > 1) {
      onPageChange(currentPage - 1);
    }
  };

  const handleNext = () => {
    if (currentPage < totalPages) {
      onPageChange(currentPage + 1);
    }
  };

  const pageNumbers = generatePageNumbers();

  return (
    <div className="flex flex-col items-center space-y-4 mt-12 mb-8">
      {/* Page info */}
      <div className="text-sm text-gray-600 font-medium">
        Page <span className="text-gray-900">{currentPage}</span> of{" "}
        <span className="text-gray-900">{totalPages}</span>
      </div>

      {/* Pagination controls */}
      <nav className="flex items-center space-x-2" aria-label="Pagination">
        {/* Previous button */}
        <button
          onClick={handlePrevious}
          disabled={currentPage === 1}
          className={`group relative flex items-center px-4 py-2.5 text-sm font-medium rounded-lg transition-all duration-200 ${
            currentPage === 1
              ? "bg-gray-100 text-gray-400 cursor-not-allowed"
              : "bg-white text-gray-700 border border-gray-300 hover:bg-gray-50 hover:border-gray-400 shadow-sm hover:shadow focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          }`}
          aria-label="Previous page"
        >
          <svg
            className="h-4 w-4 mr-2 transition-transform group-hover:-translate-x-0.5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M15 19l-7-7 7-7"
            />
          </svg>
          Previous
        </button>

        {/* Page numbers */}
        <div className="flex items-center space-x-1">
          {pageNumbers.map((page, index) => {
            if (page === "ellipsis1" || page === "ellipsis2") {
              return (
                <span
                  key={`ellipsis-${index}`}
                  className="flex items-center justify-center w-10 h-10 text-gray-500 font-medium"
                  aria-hidden="true"
                >
                  <svg
                    className="w-5 h-5"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <circle cx="4" cy="10" r="1.5" />
                    <circle cx="10" cy="10" r="1.5" />
                    <circle cx="16" cy="10" r="1.5" />
                  </svg>
                </span>
              );
            }

            return (
              <button
                key={`page-${page}`}
                onClick={() => onPageChange(Number(page))}
                className={`relative flex items-center justify-center w-10 h-10 text-sm font-semibold rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${
                  currentPage === page
                    ? "bg-blue-600 text-white shadow-lg transform scale-105"
                    : "bg-white text-gray-700 border border-gray-300 hover:bg-gray-50 hover:border-gray-400 shadow-sm hover:shadow"
                }`}
                aria-label={`Page ${page}`}
                aria-current={currentPage === page ? "page" : undefined}
              >
                {page}
                {currentPage === page && (
                  <span className="absolute inset-0 rounded-lg ring-2 ring-blue-300 ring-opacity-50"></span>
                )}
              </button>
            );
          })}
        </div>

        {/* Next button */}
        <button
          onClick={handleNext}
          disabled={currentPage === totalPages}
          className={`group relative flex items-center px-4 py-2.5 text-sm font-medium rounded-lg transition-all duration-200 ${
            currentPage === totalPages
              ? "bg-gray-100 text-gray-400 cursor-not-allowed"
              : "bg-white text-gray-700 border border-gray-300 hover:bg-gray-50 hover:border-gray-400 shadow-sm hover:shadow focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          }`}
          aria-label="Next page"
        >
          Next
          <svg
            className="h-4 w-4 ml-2 transition-transform group-hover:translate-x-0.5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 5l7 7-7 7"
            />
          </svg>
        </button>
      </nav>

      {/* Quick jump info for better UX */}
      {totalPages > 10 && (
        <div className="text-xs text-gray-500 max-w-sm text-center leading-relaxed">
          Use the page numbers to jump quickly through results
        </div>
      )}
    </div>
  );
};

export default Pagination;
