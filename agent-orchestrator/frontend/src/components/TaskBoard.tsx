import type { SubTask, TaskStatus } from '../types';

interface TaskBoardProps {
  subtasks: SubTask[];
  onSubtaskClick?: (subtask: SubTask) => void;
}

const STATUS_COLUMNS: { status: TaskStatus; label: string }[] = [
  { status: 'pending', label: 'Pending' },
  { status: 'in_progress', label: 'In Progress' },
  { status: 'completed', label: 'Completed' },
  { status: 'failed', label: 'Failed' },
];

const COMPLEXITY_COLORS: Record<string, string> = {
  simple: '#4ade80',    // green
  medium: '#fbbf24',    // yellow
  complex: '#f87171',   // red
};

export function TaskBoard({ subtasks, onSubtaskClick }: TaskBoardProps) {
  const getSubtasksByStatus = (status: TaskStatus): SubTask[] => {
    return subtasks.filter((st) => st.status === status);
  };

  return (
    <div className="task-board">
      {STATUS_COLUMNS.map(({ status, label }) => (
        <div key={status} className="task-board__column">
          <h3 className="task-board__column-header">
            {label}
            <span className="task-board__count">
              {getSubtasksByStatus(status).length}
            </span>
          </h3>

          <div className="task-board__cards">
            {getSubtasksByStatus(status).map((subtask) => (
              <div
                key={subtask.id}
                className="task-board__card"
                onClick={() => onSubtaskClick?.(subtask)}
              >
                <div className="task-board__card-header">
                  <span
                    className="task-board__complexity"
                    style={{ backgroundColor: COMPLEXITY_COLORS[subtask.complexity] }}
                  >
                    {subtask.complexity}
                  </span>
                </div>

                <h4 className="task-board__card-title">{subtask.title}</h4>

                <p className="task-board__card-description">
                  {subtask.description.slice(0, 100)}
                  {subtask.description.length > 100 && '...'}
                </p>

                {subtask.dependencies.length > 0 && (
                  <div className="task-board__dependencies">
                    Depends on: {subtask.dependencies.length} task(s)
                  </div>
                )}
              </div>
            ))}

            {getSubtasksByStatus(status).length === 0 && (
              <p className="task-board__empty">No tasks</p>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
