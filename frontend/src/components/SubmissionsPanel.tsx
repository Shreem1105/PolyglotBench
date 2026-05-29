import { useEffect, useState } from "react";

import { getSubmissions } from "../api/client";
import type { SubmissionResponse } from "../types/api";

type SubmissionsPanelProps = {
  refreshKey?: number;
};

function formatTimestamp(value: string): string {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }
  return date.toLocaleString();
}

export default function SubmissionsPanel({ refreshKey = 0 }: SubmissionsPanelProps) {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [submissions, setSubmissions] = useState<SubmissionResponse[]>([]);

  useEffect(() => {
    let cancelled = false;

    async function loadSubmissions() {
      setLoading(true);
      setError(null);

      try {
        const response = await getSubmissions(20);
        if (!cancelled) {
          setSubmissions(response.submissions);
        }
      } catch (loadError) {
        if (!cancelled) {
          setError(
            loadError instanceof Error ? loadError.message : "Failed to load submissions."
          );
          setSubmissions([]);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    loadSubmissions();

    return () => {
      cancelled = true;
    };
  }, [refreshKey]);

  if (loading) {
    return <p className="panel-hint">Loading recent submissions...</p>;
  }

  if (error) {
    return <div className="status-banner error">{error}</div>;
  }

  if (submissions.length === 0) {
    return <p className="panel-hint">No saved submissions yet.</p>;
  }

  return (
    <div className="submissions-table-wrap">
      <table className="submissions-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Language</th>
            <th>Models</th>
            <th>Baseline</th>
            <th>Min Fairness</th>
            <th>Max Token Multiplier</th>
            <th>Created At</th>
          </tr>
        </thead>
        <tbody>
          {submissions.map((submission) => (
            <tr key={submission.id}>
              <td>{submission.id}</td>
              <td>{submission.language_detected}</td>
              <td>{submission.selected_models.join(", ")}</td>
              <td>{submission.baseline_model_id}</td>
              <td>{submission.min_fairness_score.toFixed(2)}</td>
              <td>{`${submission.max_token_multiplier.toFixed(2)}x`}</td>
              <td>{formatTimestamp(submission.created_at)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
