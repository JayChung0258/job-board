import React from "react";
import { Job } from "../types/job";

interface JobCardProps {
  job: Job;
}

const JobCard: React.FC<JobCardProps> = ({ job }) => {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    }).format(date);
  };

  const renderTags = (category: string, tags?: string[]) => {
    if (!tags || tags.length === 0) return null;

    const tagColorClasses: Record<string, string> = {
      role: "bg-blue-100 text-blue-800",
      technology: "bg-green-100 text-green-800",
      skill: "bg-purple-100 text-purple-800",
      methodology: "bg-yellow-100 text-yellow-800",
      tool: "bg-red-100 text-red-800",
    };

    const colorClass = tagColorClasses[category] || "bg-gray-100 text-gray-800";

    return (
      <div className="mt-2">
        <span className="text-xs font-medium text-gray-500 uppercase">
          {category}:
        </span>
        <div className="flex flex-wrap gap-1 mt-1">
          {tags.map((tag) => (
            <span
              key={`${category}-${tag}`}
              className={`text-xs px-2 py-1 rounded-full ${colorClass}`}
            >
              {tag.replace(/-/g, " ")}
            </span>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200 hover:shadow-lg transition-shadow">
      <div className="flex justify-between items-start mb-3">
        <h3 className="text-xl font-bold text-gray-800">{job.job_position}</h3>
        <span className="text-sm text-gray-500">
          {formatDate(job.job_posting_date)}
        </span>
      </div>

      <div className="mb-3">
        <span className="text-lg font-medium text-gray-700">
          {job.company_name}
        </span>
        <div className="text-sm text-gray-600 mt-1">
          <span>{job.job_location}</span>
        </div>
      </div>

      <div className="mt-4 space-y-2">
        {renderTags("role", job.tags.role)}
        {renderTags("technology", job.tags.technology)}
        {renderTags("skill", job.tags.skill)}
        {renderTags("methodology", job.tags.methodology)}
        {renderTags("tool", job.tags.tool)}
      </div>

      <div className="mt-6">
        <a
          href={job.job_link}
          target="_blank"
          rel="noopener noreferrer"
          className="text-blue-600 hover:text-blue-800 font-medium transition-colors"
        >
          View Job →
        </a>
      </div>
    </div>
  );
};

export default JobCard;
