import { useEffect, useState } from 'react';
import { costApi } from '../api';
import type { CostSummary } from '../types';

interface CostDashboardProps {
  refreshInterval?: number; // ms, default 30000
}

export function CostDashboard({ refreshInterval = 30000 }: CostDashboardProps) {
  const [costs, setCosts] = useState<CostSummary | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const fetchCosts = async () => {
    try {
      const summary = await costApi.getSummary();
      setCosts(summary);
      setError(null);
    } catch (err: any) {
      setError('Failed to load cost data');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchCosts();
    const interval = setInterval(fetchCosts, refreshInterval);
    return () => clearInterval(interval);
  }, [refreshInterval]);

  if (isLoading) {
    return <div className="cost-dashboard cost-dashboard--loading">Loading costs...</div>;
  }

  if (error || !costs) {
    return <div className="cost-dashboard cost-dashboard--error">{error}</div>;
  }

  const isOverBudget = costs.budget_percent_used >= 100;
  const isWarning = costs.budget_percent_used >= 80;

  return (
    <div className={`cost-dashboard ${isOverBudget ? 'cost-dashboard--danger' : isWarning ? 'cost-dashboard--warning' : ''}`}>
      <h3 className="cost-dashboard__title">Today's Usage</h3>

      <div className="cost-dashboard__grid">
        <div className="cost-dashboard__stat">
          <span className="cost-dashboard__label">Cloud LLM Cost</span>
          <span className="cost-dashboard__value">${costs.today_cloud_usd.toFixed(4)}</span>
        </div>

        <div className="cost-dashboard__stat">
          <span className="cost-dashboard__label">Budget Remaining</span>
          <span className="cost-dashboard__value">${costs.budget_remaining_usd.toFixed(2)}</span>
        </div>

        <div className="cost-dashboard__stat">
          <span className="cost-dashboard__label">Input Tokens</span>
          <span className="cost-dashboard__value">{costs.today_tokens_input.toLocaleString()}</span>
        </div>

        <div className="cost-dashboard__stat">
          <span className="cost-dashboard__label">Output Tokens</span>
          <span className="cost-dashboard__value">{costs.today_tokens_output.toLocaleString()}</span>
        </div>
      </div>

      <div className="cost-dashboard__progress">
        <div className="cost-dashboard__progress-bar">
          <div
            className="cost-dashboard__progress-fill"
            style={{ width: `${Math.min(costs.budget_percent_used, 100)}%` }}
          />
        </div>
        <span className="cost-dashboard__progress-label">
          {costs.budget_percent_used.toFixed(1)}% of ${costs.budget_limit_usd} daily budget
        </span>
      </div>

      {isOverBudget && (
        <p className="cost-dashboard__alert">
          ⚠️ Daily budget exceeded! Cloud LLM calls are blocked.
        </p>
      )}
    </div>
  );
}
