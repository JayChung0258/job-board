import React from "react";
import { Job } from "../types/job";

interface JobCardProps {
  job: Job;
}

/**
 * Compact Modern JobCard Component
 *
 * Clean, minimal job card with compact layout and modern design.
 * Features hover animations, tag organization, and optimized space usage.
 */
const JobCard: React.FC<JobCardProps> = ({ job }) => {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - date.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 1) return "1d ago";
    if (diffDays < 7) return `${diffDays}d ago`;
    if (diffDays < 30) return `${Math.floor(diffDays / 7)}w ago`;
    return date.toLocaleDateString("en-US", { month: "short", day: "numeric" });
  };

  const getAllTags = () => {
    const allTags: { tag: string; category: string }[] = [];

    Object.entries(job.tags).forEach(([category, tags]) => {
      if (tags && tags.length > 0) {
        tags.forEach((tag: string) => {
          allTags.push({ tag: tag.replace(/-/g, " "), category });
        });
      }
    });

    return allTags.slice(0, 6); // Limit to 6 tags for compact layout
  };

  const getTagColor = (category: string) => {
    const colors: Record<string, string> = {
      role: "bg-purple-50 text-purple-700 border-purple-200",
      technology: "bg-blue-50 text-blue-700 border-blue-200",
      skill: "bg-green-50 text-green-700 border-green-200",
      methodology: "bg-yellow-50 text-yellow-700 border-yellow-200",
      tool: "bg-pink-50 text-pink-700 border-pink-200",
    };
    return colors[category] || "bg-gray-50 text-gray-700 border-gray-200";
  };

  const tags = getAllTags();

  return (
    <div className="group relative bg-white rounded-lg border border-gray-200 hover:border-blue-300 transition-all duration-200 hover:shadow-md overflow-hidden">
      {/* Top accent line */}
      <div className="absolute top-0 left-0 h-0.5 w-full bg-gradient-to-r from-blue-500 to-purple-500 transform scale-x-0 origin-left transition-transform duration-300 group-hover:scale-x-100"></div>

      <div className="p-4">
        {/* Header with title and date */}
        <div className="flex justify-between items-start mb-2">
          <h3 className="font-semibold text-gray-900 group-hover:text-blue-600 transition-colors duration-200 line-clamp-2 leading-tight">
            {job.job_position}
          </h3>
          <span className="text-xs text-gray-500 ml-2 whitespace-nowrap">
            {formatDate(job.job_posting_date)}
          </span>
        </div>

        {/* Company and location */}
        <div className="flex items-center justify-between mb-3">
          <span className="font-medium text-gray-700 text-sm truncate">
            {job.company_name}
          </span>
          <div className="flex items-center text-xs text-gray-600 bg-gray-50 px-2 py-1 rounded-full ml-2">
            <svg
              className="h-3 w-3 mr-1 flex-shrink-0"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fillRule="evenodd"
                d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z"
                clipRule="evenodd"
              />
            </svg>
            <span className="truncate">{job.job_location}</span>
          </div>
        </div>

        {/* Compact tags */}
        {tags.length > 0 && (
          <div className="flex flex-wrap gap-1 mb-3">
            {tags.map((item, index) => (
              <span
                key={`${item.category}-${item.tag}-${index}`}
                className={`inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium border ${getTagColor(
                  item.category,
                )}`}
              >
                {item.tag}
              </span>
            ))}
            {Object.values(job.tags).flat().length > 6 && (
              <span className="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium bg-gray-100 text-gray-600 border border-gray-200">
                +{Object.values(job.tags).flat().length - 6}
              </span>
            )}
          </div>
        )}

        {/* Footer with action and save buttons */}
        <div className="flex items-center justify-between pt-2 border-t border-gray-100">
          <a
            href={job.job_link}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center text-sm font-medium text-blue-600 hover:text-blue-700 transition-colors group/link"
          >
            View Job
            <svg
              className="ml-1 h-3 w-3 transition-transform group-hover/link:translate-x-0.5"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fillRule="evenodd"
                d="M10.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L12.586 11H5a1 1 0 110-2h7.586l-2.293-2.293a1 1 0 010-1.414z"
                clipRule="evenodd"
              />
            </svg>
          </a>

          <div className="flex items-center space-x-1">
            <button
              className="p-1.5 text-gray-400 hover:text-red-500 bg-white hover:bg-red-50 rounded-md transition-colors duration-200 border border-gray-200"
              title="Save job"
            >
              <svg className="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                <path d="M5 4a2 2 0 012-2h6a2 2 0 012 2v14l-5-2.5L5 18V4z" />
              </svg>
            </button>
            <button
              className="p-1.5 text-gray-400 hover:text-blue-500 bg-white hover:bg-blue-50 rounded-md transition-colors duration-200 border border-gray-200"
              title="Share job"
            >
              <svg className="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
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
