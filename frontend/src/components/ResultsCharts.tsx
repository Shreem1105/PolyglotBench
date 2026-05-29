import {
  Bar,
  BarChart,
  CartesianGrid,
  LabelList,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import type { ModelAnalysis } from "../types/api";

type ResultsChartsProps = {
  analyses: ModelAnalysis[];
};

type ChartDatum = {
  model: string;
  token_count: number;
  token_multiplier: number;
  estimated_latency_multiplier: number;
  fairness_score: number;
};

function toChartData(analyses: ModelAnalysis[]): ChartDatum[] {
  return analyses.map((item) => ({
    model: item.display_name || item.model_id,
    token_count: item.token_count,
    token_multiplier: item.token_multiplier,
    estimated_latency_multiplier: item.estimated_latency_multiplier,
    fairness_score: item.fairness_score,
  }));
}

function toNumber(value: number | string | undefined): number {
  if (typeof value === "number") {
    return value;
  }
  if (typeof value === "string") {
    const parsed = Number(value);
    return Number.isFinite(parsed) ? parsed : 0;
  }
  return 0;
}

function multiplierLabel(value: number | string | undefined): string {
  return `${toNumber(value).toFixed(2)}x`;
}

function scoreLabel(value: number | string | undefined): string {
  return `${toNumber(value).toFixed(2)} / 100`;
}

export default function ResultsCharts({ analyses }: ResultsChartsProps) {
  const data = toChartData(analyses);

  return (
    <div className="chart-grid">
      <article className="chart-card">
        <h4>Token Count Comparison</h4>
        <p className="chart-note">Higher bars indicate more tokenizer fragments for the same text.</p>
        <div className="chart-wrap">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data} margin={{ top: 12, right: 10, left: 0, bottom: 42 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#dbe5ec" />
              <XAxis dataKey="model" angle={-18} textAnchor="end" interval={0} height={56} />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Bar dataKey="token_count" fill="#2b7cab" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </article>

      <article className="chart-card">
        <h4>Token Multiplier and Estimated Latency</h4>
        <p className="chart-note">
          Estimated latency currently equals token multiplier in this MVP proxy model.
        </p>
        <div className="chart-wrap">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data} margin={{ top: 12, right: 10, left: 0, bottom: 42 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#dbe5ec" />
              <XAxis dataKey="model" angle={-18} textAnchor="end" interval={0} height={56} />
              <YAxis />
              <Tooltip formatter={(value) => multiplierLabel(value as number | string | undefined)} />
              <Bar
                dataKey="token_multiplier"
                fill="#4e6fd0"
                name="Token Multiplier"
                radius={[6, 6, 0, 0]}
              >
                <LabelList
                  dataKey="token_multiplier"
                  position="top"
                  formatter={(value) =>
                    multiplierLabel(value as number | string | undefined)
                  }
                />
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </article>

      <article className="chart-card chart-card-wide">
        <h4>Fairness Score Comparison</h4>
        <p className="chart-note">
          Higher scores suggest fairer tokenizer efficiency relative to the selected baseline.
        </p>
        <div className="chart-wrap">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data} margin={{ top: 12, right: 10, left: 0, bottom: 42 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#dbe5ec" />
              <XAxis dataKey="model" angle={-18} textAnchor="end" interval={0} height={56} />
              <YAxis domain={[0, 100]} />
              <Tooltip formatter={(value) => scoreLabel(value as number | string | undefined)} />
              <Bar dataKey="fairness_score" fill="#1f9d6b" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </article>
    </div>
  );
}
