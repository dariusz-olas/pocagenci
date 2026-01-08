// Task types
export type TaskStatus = 'pending' | 'decomposing' | 'ready' | 'in_progress' | 'completed' | 'failed';
export type SubTaskComplexity = 'simple' | 'medium' | 'complex';
export type ExecutionStatus = 'queued' | 'running' | 'completed' | 'failed' | 'cancelled';

export interface SubTask {
  id: string;
  title: string;
  description: string;
  complexity: SubTaskComplexity;
  status: TaskStatus;
  dependencies: string[];
  acceptance_criteria: string[];
}

export interface Task {
  id: string;
  description: string;
  status: TaskStatus;
  subtasks: SubTask[];
  created_at: string;
  updated_at: string | null;
}

export interface TaskDecomposition {
  original_task: string;
  subtasks: Omit<SubTask, 'id' | 'status'>[];
  execution_order: string[][];
  estimated_cost_usd: number;
}

// Execution types
export interface ExecutionLogEntry {
  timestamp: string;
  level: 'info' | 'warning' | 'error';
  message: string;
  agent?: string;
}

export interface Execution {
  id: string;
  task_id: string;
  status: ExecutionStatus;
  output: string | null;
  logs: ExecutionLogEntry[];
  started_at: string | null;
  completed_at: string | null;
  execution_time_seconds: number | null;
}

export interface ExecutionProgress {
  execution_id: string;
  type: 'status' | 'log' | 'complete' | 'error' | 'connected';
  data: Record<string, unknown>;
}

// Cost types
export interface CostSummary {
  today_cloud_usd: number;
  today_tokens_input: number;
  today_tokens_output: number;
  budget_limit_usd: number;
  budget_remaining_usd: number;
  budget_percent_used: number;
}

// API types
export interface ApiError {
  detail: string | { error: string; message: string };
}
