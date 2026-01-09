import axios, { AxiosInstance } from 'axios';
import type { Task, TaskDecomposition, Execution, CostSummary } from './types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const API_KEY = import.meta.env.VITE_API_KEY || 'dev-api-key-change-in-production';

// Create axios instance with default config
const api: AxiosInstance = axios.create({
  baseURL: `${API_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': API_KEY,
  },
});

// Task endpoints
export const taskApi = {
  decompose: async (description: string): Promise<TaskDecomposition> => {
    const response = await api.post<TaskDecomposition>('/tasks/decompose', { description });
    return response.data;
  },

  create: async (description: string): Promise<Task> => {
    const response = await api.post<Task>('/tasks', { description });
    return response.data;
  },

  get: async (taskId: string): Promise<Task> => {
    const response = await api.get<Task>(`/tasks/${taskId}`);
    return response.data;
  },

  execute: async (taskId: string): Promise<{ execution_id: string }> => {
    const response = await api.post<{ execution_id: string }>(`/tasks/${taskId}/execute`);
    return response.data;
  },
};

// Execution endpoints
export const executionApi = {
  get: async (executionId: string): Promise<Execution> => {
    const response = await api.get<Execution>(`/executions/${executionId}`);
    return response.data;
  },
};

// Cost endpoints
export const costApi = {
  getSummary: async (): Promise<CostSummary> => {
    const response = await api.get<CostSummary>('/costs/summary');
    return response.data;
  },
};

// Health check (no auth required)
export const healthApi = {
  check: async (): Promise<{ status: string; checks: Record<string, boolean> }> => {
    const response = await axios.get(`${API_URL}/health`);
    return response.data;
  },
};

export default api;
