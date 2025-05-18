export interface Tag {
  id: number;
  name: string;
  category: string;
  description?: string;
}

export interface JobTags {
  role?: string[];
  technology?: string[];
  skill?: string[];
  methodology?: string[];
  tool?: string[];
}

export interface Job {
  id: number;
  job_id: string;
  job_position: string;
  job_link: string;
  company_name: string;
  company_profile?: string;
  job_location: string;
  job_posting_date: string;
  tags: JobTags;
  created_at?: string;
  updated_at?: string;
}

export interface JobSearchParams {
  query?: string;
  location?: string;
  tags?: string[];
  tag_categories?: string[];
  date_from?: string;
  date_to?: string;
  page?: number;
  limit?: number;
}

export interface JobSearchResponse {
  items: Job[];
  total: number;
  page: number;
  limit: number;
  pages: number;
}
