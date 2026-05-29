import type { ModelAnalysis } from "../types/api";

type ResultsTableProps = {
  analyses: ModelAnalysis[];
};

function formatMultiplier(value: number): string {
  return `${value.toFixed(2)}x`;
}

function formatCost(value: number): string {
  return `$${value.toFixed(8)}`;
}

function formatFairness(value: number): string {
  return `${value.toFixed(2)} / 100`;
}

export default function ResultsTable({ analyses }: ResultsTableProps) {
  return (
    <div className="results-table-wrap">
      <table className="results-table">
        <thead>
          <tr>
            <th>Model</th>
            <th>Provider</th>
            <th>Tokens</th>
            <th>Words</th>
            <th>Fertility</th>
            <th>Token Multiplier</th>
            <th>Estimated Latency</th>
            <th>Estimated Cost</th>
            <th>Fairness Score</th>
          </tr>
        </thead>
        <tbody>
          {analyses.map((analysis) => (
            <tr key={analysis.model_id}>
              <td>{analysis.display_name}</td>
              <td>{analysis.provider}</td>
              <td>{analysis.token_count}</td>
              <td>{analysis.word_count}</td>
              <td>{analysis.fertility.toFixed(4)}</td>
              <td>{formatMultiplier(analysis.token_multiplier)}</td>
              <td>{formatMultiplier(analysis.estimated_latency_multiplier)}</td>
              <td>{formatCost(analysis.input_cost_estimate_usd)}</td>
              <td>{formatFairness(analysis.fairness_score)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
