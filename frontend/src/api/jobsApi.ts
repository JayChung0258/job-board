import axios from "axios";
import qs from "qs";
import { Job, JobSearchParams, JobSearchResponse } from "../types/job";

const API_URL = "/api/v1";

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
  paramsSerializer: (params) => qs.stringify(params, { indices: false }),
});

export const searchJobs = async (
  params: JobSearchParams,
): Promise<JobSearchResponse> => {
  const response = await api.get("/jobs/search", { params });
  return response.data;
};

export const getJobById = async (id: string): Promise<Job> => {
  const response = await api.get(`/jobs/${id}`);
  return response.data;
};

export const getTagCategories = async (): Promise<string[]> => {
  const response = await api.get("/tags/categories");
  return response.data;
};

export const getTagsByCategory = async (
  category: string,
): Promise<string[]> => {
  const response = await api.get(`/tags/by-category/${category}`);
  return response.data;
};
