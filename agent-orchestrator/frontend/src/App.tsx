import { useState } from 'react';
import { TaskInput } from './components/TaskInput';
import { TaskBoard } from './components/TaskBoard';
import { CostDashboard } from './components/CostDashboard';
import type { TaskDecomposition, SubTask } from './types';
import './App.css';

function App() {
  const [decomposition, setDecomposition] = useState<TaskDecomposition | null>(null);
  const [subtasks, setSubtasks] = useState<SubTask[]>([]);
  const [error, setError] = useState<string | null>(null);

  const handleDecomposed = (result: TaskDecomposition) => {
    setDecomposition(result);
    // Convert decomposition subtasks to SubTask with id and status
    const subtasksWithIds: SubTask[] = result.subtasks.map((st, index) => ({
      ...st,
      id: `subtask-${index}`,
      status: 'pending' as const,
    }));
    setSubtasks(subtasksWithIds);
    setError(null);
  };

  const handleError = (message: string) => {
    setError(message);
  };

  const handleSubtaskClick = (subtask: SubTask) => {
    console.log('Subtask clicked:', subtask);
    // TODO: Show subtask details modal
  };

  return (
    <div className="app">
      <header className="app__header">
        <h1>Agent Orchestrator</h1>
        <p>AI-powered task decomposition and execution</p>
      </header>

      <div className="app__sidebar">
        <CostDashboard />
      </div>

      <main className="app__main">
        <section className="app__input-section">
          <TaskInput onDecomposed={handleDecomposed} onError={handleError} />

          {error && (
            <div className="app__error">
              {error}
              <button onClick={() => setError(null)}>×</button>
            </div>
          )}
        </section>

        {decomposition && (
          <section className="app__decomposition">
            <h2>Task Decomposition</h2>
            <p>
              <strong>Original:</strong> {decomposition.original_task}
            </p>
            <p>
              <strong>Estimated cost:</strong> ${decomposition.estimated_cost_usd.toFixed(4)}
            </p>
            <p>
              <strong>Subtasks:</strong> {decomposition.subtasks.length}
            </p>
          </section>
        )}

        {subtasks.length > 0 && (
          <section className="app__board-section">
            <h2>Subtasks</h2>
            <TaskBoard subtasks={subtasks} onSubtaskClick={handleSubtaskClick} />
          </section>
        )}
      </main>
    </div>
  );
}

export default App;
