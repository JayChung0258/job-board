import React, { useState, useEffect } from "react";
import { getTagCategories, getTagsByCategory } from "../api/jobsApi";

interface JobFilterProps {
  onFilterApply: (filters: FilterState) => void;
  onFilterReset: () => void;
}

export interface FilterState {
  selectedTags: Record<string, string[]>;
  salaryRange: [number, number];
  salaryFilterActive: boolean;
}

const JobFilter: React.FC<JobFilterProps> = ({
  onFilterApply,
  onFilterReset,
}) => {
  const [filters, setFilters] = useState<FilterState>({
    selectedTags: {},
    salaryRange: [50, 150],
    salaryFilterActive: false,
  });

  // State for dynamic tag data
  const [tagCategories, setTagCategories] = useState<string[]>([]);
  const [availableTags, setAvailableTags] = useState<Record<string, string[]>>(
    {},
  );
  const [loadingTags, setLoadingTags] = useState(false);

  // Accordion states for collapsible sections
  const [openSections, setOpenSections] = useState<Record<string, boolean>>({
    salary: false,
  });

  // Load tag categories on mount
  useEffect(() => {
    const loadTagCategories = async () => {
      try {
        setLoadingTags(true);
        const categories = await getTagCategories();
        setTagCategories(categories);

        // Initialize openSections for tag categories
        const newOpenSections = { ...openSections };
        categories.forEach((category) => {
          newOpenSections[category] = false; // Start closed for tag categories
        });
        setOpenSections(newOpenSections);
      } catch (error) {
        console.error("Failed to load tag categories:", error);
      } finally {
        setLoadingTags(false);
      }
    };

    loadTagCategories();
  }, []);

  // Load tags for a specific category when section is opened
  const loadTagsForCategory = async (category: string) => {
    if (availableTags[category]) return; // Already loaded

    try {
      const tags = await getTagsByCategory(category);
      setAvailableTags((prev) => ({
        ...prev,
        [category]: tags,
      }));
    } catch (error) {
      console.error(`Failed to load tags for ${category}:`, error);
    }
  };

  const toggleSection = (section: string) => {
    setOpenSections((prev) => {
      const newOpenSections = {
        ...prev,
        [section]: !prev[section],
      };

      // Load tags when opening a tag category section
      if (newOpenSections[section] && tagCategories.includes(section)) {
        loadTagsForCategory(section);
      }

      return newOpenSections;
    });
  };

  const handleTagChange = (category: string, tag: string) => {
    setFilters((prev) => {
      const currentTags = prev.selectedTags[category] || [];
      const newTags = currentTags.includes(tag)
        ? currentTags.filter((t) => t !== tag)
        : [...currentTags, tag];

      return {
        ...prev,
        selectedTags: {
          ...prev.selectedTags,
          [category]: newTags,
        },
      };
    });
  };

  const handleSalaryMinChange = (value: number) => {
    setFilters((prev) => ({
      ...prev,
      salaryRange: [value, Math.max(value, prev.salaryRange[1])],
    }));
  };

  const handleSalaryMaxChange = (value: number) => {
    setFilters((prev) => ({
      ...prev,
      salaryRange: [Math.min(prev.salaryRange[0], value), value],
    }));
  };

  const toggleSalaryFilter = () => {
    setFilters((prev) => ({
      ...prev,
      salaryFilterActive: !prev.salaryFilterActive,
    }));
  };

  const handleApplyFilters = () => {
    onFilterApply(filters);
  };

  const handleResetFilters = () => {
    const resetFilters: FilterState = {
      selectedTags: {},
      salaryRange: [50, 150],
      salaryFilterActive: false,
    };
    setFilters(resetFilters);
    onFilterReset();
  };

  const FilterSection = ({
    id,
    title,
    children,
  }: {
    id: string;
    title: string;
    children: React.ReactNode;
  }) => (
    <div className="border-b border-gray-200 last:border-b-0">
      <button
        onClick={() => toggleSection(id)}
        className="flex items-center justify-between w-full py-4 px-4 text-left bg-white hover:bg-gray-50 transition-all duration-300 ease-in-out"
      >
        <h4 className="text-sm font-medium text-gray-900">{title}</h4>
        <svg
          className={`h-5 w-5 text-gray-400 transform transition-transform duration-500 ease-in-out ${
            openSections[id] ? "rotate-180" : "rotate-0"
          }`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M19 9l-7 7-7-7"
          />
        </svg>
      </button>
      <div
        className={`overflow-hidden transition-all duration-500 ease-in-out ${
          openSections[id] ? "max-h-96 opacity-100" : "max-h-0 opacity-0"
        }`}
      >
        <div
          className={`px-4 pb-4 transition-all duration-500 ease-in-out transform ${
            openSections[id] ? "translate-y-0" : "-translate-y-2"
          }`}
        >
          {children}
        </div>
      </div>
    </div>
  );

  const CheckboxItem = ({
    id,
    label,
    value,
    checked,
    onChange,
  }: {
    id: string;
    label: string;
    value: string;
    checked: boolean;
    onChange: () => void;
  }) => (
    <div className="flex items-center space-x-2 py-1">
      <input type="checkbox" id={id} checked={checked} onChange={onChange} />
      <label htmlFor={id} className="text-sm text-gray-700 cursor-pointer">
        {label}
      </label>
    </div>
  );

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden sticky top-8">
      <div className="p-4 border-b border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900">Filters</h3>
      </div>

      <div className="divide-y divide-gray-200">
        {/* Dynamic Tag Categories */}
        {tagCategories.map((category) => (
          <FilterSection
            key={category}
            id={category}
            title={category.charAt(0).toUpperCase() + category.slice(1)}
          >
            <div className="space-y-2">
              {availableTags[category] ? (
                availableTags[category].map((tag) => (
                  <CheckboxItem
                    key={`${category}-${tag}`}
                    id={`${category}-${tag.toLowerCase().replace(/\s+/g, "-")}`}
                    label={tag.replace(/-/g, " ")}
                    value={tag}
                    checked={(filters.selectedTags[category] || []).includes(
                      tag,
                    )}
                    onChange={() => handleTagChange(category, tag)}
                  />
                ))
              ) : (
                <div className="text-sm text-gray-500 italic py-2">
                  Loading {category} tags...
                </div>
              )}
            </div>
          </FilterSection>
        ))}

        <FilterSection id="salary" title="Salary Range">
          <div className="space-y-4">
            <div className="flex items-center space-x-2">
              <input
                type="checkbox"
                id="salary-filter-active"
                checked={filters.salaryFilterActive}
                onChange={toggleSalaryFilter}
              />
              <label
                htmlFor="salary-filter-active"
                className="text-sm text-gray-700 cursor-pointer"
              >
                Filter by salary
              </label>
            </div>

            <div
              className={`overflow-hidden transition-all duration-500 ease-in-out ${
                filters.salaryFilterActive
                  ? "max-h-64 opacity-100"
                  : "max-h-0 opacity-0"
              }`}
            >
              <div
                className={`space-y-3 pt-2 transition-all duration-500 ease-in-out transform ${
                  filters.salaryFilterActive
                    ? "translate-y-0"
                    : "-translate-y-2"
                }`}
              >
                <div>
                  <label className="block text-xs font-medium text-gray-700 mb-1">
                    Minimum Salary: ${filters.salaryRange[0]}k
                  </label>
                  <input
                    type="range"
                    min="0"
                    max="300"
                    step="5"
                    value={filters.salaryRange[0]}
                    onChange={(e) =>
                      handleSalaryMinChange(parseInt(e.target.value))
                    }
                    className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-700 mb-1">
                    Maximum Salary: ${filters.salaryRange[1]}k
                  </label>
                  <input
                    type="range"
                    min="0"
                    max="300"
                    step="5"
                    value={filters.salaryRange[1]}
                    onChange={(e) =>
                      handleSalaryMaxChange(parseInt(e.target.value))
                    }
                    className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
                  />
                </div>
                <div className="flex items-center justify-between text-sm text-gray-700 bg-gray-50 rounded-md px-3 py-2">
                  <span>${filters.salaryRange[0]}k</span>
                  <span className="text-gray-400">-</span>
                  <span>${filters.salaryRange[1]}k</span>
                </div>
              </div>
            </div>

            {!filters.salaryFilterActive && (
              <p className="text-xs text-gray-500 italic">
                Some jobs don't disclose salary information
              </p>
            )}
          </div>
        </FilterSection>
      </div>

      {/* Action Buttons */}
      <div className="p-4 space-y-2 border-t border-gray-200">
        <button
          onClick={handleApplyFilters}
          className="w-full bg-gray-900 text-white py-2 px-4 rounded-lg text-sm font-medium hover:bg-gray-800 transition-all duration-300 ease-in-out transform hover:scale-105 active:scale-95"
        >
          Apply Filters
        </button>
        <button
          onClick={handleResetFilters}
          className="w-full bg-white text-gray-700 py-2 px-4 rounded-lg text-sm font-medium border border-gray-300 hover:bg-gray-50 transition-all duration-300 ease-in-out transform hover:scale-105 active:scale-95"
        >
          Reset
        </button>
      </div>
    </div>
  );
};

export default JobFilter;
