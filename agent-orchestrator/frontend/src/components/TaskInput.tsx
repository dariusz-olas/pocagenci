import { useState } from 'react';
import { taskApi } from '../api';
import type { TaskDecomposition } from '../types';

interface TaskInputProps {
  onDecomposed?: (decomposition: TaskDecomposition) => void;
  onError?: (error: string) => void;
}

export function TaskInput({ onDecomposed, onError }: TaskInputProps) {
  const [description, setDescription] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!description.trim() || description.length < 10) {
      onError?.('Task description must be at least 10 characters');
      return;
    }

    setIsLoading(true);

    try {
      const decomposition = await taskApi.decompose(description);
      onDecomposed?.(decomposition);
      setDescription('');
    } catch (err: any) {
      const message = err.response?.data?.detail || 'Failed to decompose task';
      onError?.(typeof message === 'string' ? message : message.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="task-input">
      <div className="task-input__field">
        <label htmlFor="task-description">Describe your task:</label>
        <textarea
          id="task-description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="e.g., Create a REST API endpoint for user authentication with JWT tokens..."
          rows={4}
          disabled={isLoading}
          minLength={10}
          maxLength={5000}
        />
        <span className="task-input__count">{description.length} / 5000</span>
      </div>

      <button
        type="submit"
        disabled={isLoading || description.length < 10}
        className="task-input__submit"
      >
        {isLoading ? 'Decomposing...' : 'Decompose Task'}
      </button>

      {isLoading && (
        <p className="task-input__info">
          Using Claude to analyze and decompose your task...
        </p>
      )}
    </form>
  );
}
