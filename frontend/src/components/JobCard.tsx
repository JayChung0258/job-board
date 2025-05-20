import React from "react";
import { Job } from "../types/job";

interface JobCardProps {
  job: Job;
}

const JobCard: React.FC<JobCardProps> = ({ job }) => {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - date.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 1) {
      return "1 day ago";
    } else if (diffDays < 7) {
      return `${diffDays} days ago`;
    } else if (diffDays < 30) {
      const weeks = Math.floor(diffDays / 7);
      return `${weeks} ${weeks === 1 ? "week" : "weeks"} ago`;
    } else {
      return date.toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
      });
    }
  };

  const renderTags = (category: string, tags: string[] = []) => {
    if (!tags || tags.length === 0) return null;

    const colorClasses: Record<string, string> = {
      role: "bg-purple-100 text-purple-800",
      technology: "bg-blue-100 text-blue-800",
      skill: "bg-green-100 text-green-800",
      methodology: "bg-yellow-100 text-yellow-800",
      tool: "bg-pink-100 text-pink-800",
    };

    const displayCategory =
      category.charAt(0).toUpperCase() + category.slice(1);

    return (
      <div>
        <span className="text-xs font-medium text-gray-500">
          {displayCategory}:
        </span>
        <div className="flex flex-wrap gap-1.5 mt-1">
          {tags.map((tag) => (
            <span
              key={tag}
              className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${
                colorClasses[category] || "bg-gray-100 text-gray-800"
              }`}
            >
              {tag.replace(/-/g, " ")}
            </span>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="group relative bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden transition-all duration-300 hover:shadow-lg hover:border-blue-200">
      <div className="absolute top-0 left-0 h-full w-1 bg-blue-600 transform scale-y-0 origin-bottom transition-transform duration-300 group-hover:scale-y-100"></div>

      <div className="p-6">
        <div className="flex flex-col sm:flex-row justify-between sm:items-start mb-3">
          <h3 className="text-xl font-bold text-gray-900 group-hover:text-blue-600 transition-colors duration-300">
            {job.job_position}
          </h3>
          <span className="mt-2 sm:mt-0 text-sm text-gray-500 whitespace-nowrap">
            {formatDate(job.job_posting_date)}
          </span>
        </div>

        <div className="mb-4">
          <div className="flex items-center">
            <span className="text-lg font-medium text-gray-800 mr-3">
              {job.company_name}
            </span>
            <span className="flex items-center text-sm px-2.5 py-0.5 rounded-full text-blue-800 bg-blue-100">
              <svg
                className="h-3 w-3 mr-1"
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
              {job.job_location}
            </span>
          </div>
        </div>

        <div className="mt-6 space-y-3">
          {renderTags("role", job.tags.role)}
          {renderTags("technology", job.tags.technology)}
          {renderTags("skill", job.tags.skill)}
          {renderTags("methodology", job.tags.methodology)}
          {renderTags("tool", job.tags.tool)}
        </div>

        <div className="mt-6 pt-4 border-t border-gray-100 flex justify-between items-center">
          <a
            href={job.job_link}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center text-blue-600 hover:text-blue-800 font-medium transition-colors"
          >
            View Job
            <svg
              className="ml-1 h-4 w-4"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fillRule="evenodd"
                d="M10.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L12.586 11H5a1 1 0 110-2h7.586l-2.293-2.293a1 1 0 010-1.414z"
                clipRule="evenodd"
              />
            </svg>
          </a>

          <div className="flex space-x-2">
            <button className="text-gray-400 hover:text-gray-600 p-1 rounded-full hover:bg-gray-100 transition-colors">
              <svg
                className="h-5 w-5"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path d="M5 4a2 2 0 012-2h6a2 2 0 012 2v14l-5-2.5L5 18V4z" />
              </svg>
            </button>
            <button className="text-gray-400 hover:text-gray-600 p-1 rounded-full hover:bg-gray-100 transition-colors">
              <svg
                className="h-5 w-5"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path d="M15 8a3 3 0 10-2.977-2.63l-4.94 2.47a3 3 0 100 4.319l4.94 2.47a3 3 0 10.895-1.789l-4.94-2.47a3.027 3.027 0 000-.74l4.94-2.47C13.456 7.68 14.19 8 15 8z" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default JobCard;
