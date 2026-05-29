import type { LeaderboardRow } from "../types/api";

type LeaderboardTableProps = {
  rows: LeaderboardRow[];
};

export default function LeaderboardTable({ rows }: LeaderboardTableProps) {
  return (
    <div className="leaderboard-table-wrap">
      <table className="leaderboard-table">
        <thead>
          <tr>
            <th>Rank</th>
            <th>Model</th>
            <th>Average Fairness Score</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.model_id}>
              <td>{row.rank}</td>
              <td>{row.model_id}</td>
              <td>{row.average_fairness_score.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
