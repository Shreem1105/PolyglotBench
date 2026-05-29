import { useEffect, useMemo, useState } from "react";
import type { FormEvent } from "react";

import { analyzeText, getLeaderboard, getModels } from "./api/client";
import LeaderboardTable from "./components/LeaderboardTable";
import MetricCard from "./components/MetricCard";
import MetricExplainer from "./components/MetricExplainer";
import ModelSelector from "./components/ModelSelector";
import ResultsCharts from "./components/ResultsCharts";
import ResultsTable from "./components/ResultsTable";
import TextInputPanel from "./components/TextInputPanel";
import type { AnalyzeResponse, LeaderboardResponse, ModelInfo } from "./types/api";

const DEFAULT_MODEL = "gpt-4o-mini";

function chooseDefaultModel(models: ModelInfo[]): string {
  if (models.some((model) => model.id === DEFAULT_MODEL)) {
    return DEFAULT_MODEL;
  }
  return models[0]?.id ?? "";
}

export default function App() {
  const [models, setModels] = useState<ModelInfo[]>([]);
  const [modelsLoading, setModelsLoading] = useState(true);
  const [modelsError, setModelsError] = useState<string | null>(null);

  const [text, setText] = useState(
    "Artificial intelligence is changing how people build software."
  );
  const [selectedModelIds, setSelectedModelIds] = useState<string[]>([]);
  const [baselineModelId, setBaselineModelId] = useState("");

  const [analyzing, setAnalyzing] = useState(false);
  const [analyzeError, setAnalyzeError] = useState<string | null>(null);
  const [result, setResult] = useState<AnalyzeResponse | null>(null);

  const [showLeaderboard, setShowLeaderboard] = useState(false);
  const [leaderboardLoading, setLeaderboardLoading] = useState(false);
  const [leaderboardError, setLeaderboardError] = useState<string | null>(null);
  const [leaderboard, setLeaderboard] = useState<LeaderboardResponse | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function loadModels() {
      setModelsLoading(true);
      setModelsError(null);

      try {
        const response = await getModels();
        if (cancelled) {
          return;
        }

        setModels(response.models);
        const defaultModel = chooseDefaultModel(response.models);
        setSelectedModelIds(defaultModel ? [defaultModel] : []);
        setBaselineModelId(defaultModel);
      } catch (error) {
        if (!cancelled) {
          setModelsError(
            error instanceof Error ? error.message : "Failed to fetch models."
          );
        }
      } finally {
        if (!cancelled) {
          setModelsLoading(false);
        }
      }
    }

    loadModels();
    return () => {
      cancelled = true;
    };
  }, []);

  function toggleModel(modelId: string) {
    setSelectedModelIds((current) => {
      if (current.includes(modelId)) {
        return current.filter((id) => id !== modelId);
      }
      return [...current, modelId];
    });
  }

  async function handleAnalyze(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setAnalyzing(true);
    setAnalyzeError(null);

    try {
      const response = await analyzeText({
        text,
        model_ids: selectedModelIds,
        baseline_model_id: baselineModelId || null,
      });
      setResult(response);
    } catch (error) {
      setAnalyzeError(
        error instanceof Error ? error.message : "Analyze request failed."
      );
      setResult(null);
    } finally {
      setAnalyzing(false);
    }
  }

  async function handleLoadLeaderboard() {
    setShowLeaderboard(true);
    setLeaderboardLoading(true);
    setLeaderboardError(null);

    try {
      const response = await getLeaderboard();
      setLeaderboard(response);
    } catch (error) {
      setLeaderboardError(
        error instanceof Error ? error.message : "Failed to load leaderboard."
      );
      setLeaderboard(null);
    } finally {
      setLeaderboardLoading(false);
    }
  }

  const summary = useMemo(() => {
    if (!result || result.analyses.length === 0) {
      return null;
    }

    const fairnessValues = result.analyses.map((item) => item.fairness_score);
    const multiplierValues = result.analyses.map((item) => item.token_multiplier);

    return {
      modelCount: result.analyses.length,
      baseline: result.baseline_model_id,
      lowestFairness: Math.min(...fairnessValues),
      highestMultiplier: Math.max(...multiplierValues),
      languageDetected: result.analyses[0]?.language_detected ?? "unknown",
    };
  }, [result]);

  return (
    <div className="app-shell">
      <header className="hero">
        <h1>PolyglotBench</h1>
        <p className="hero-subtitle">Live Tokenization Fairness Observatory</p>
        <p className="hero-description">
          Compare multilingual text across model tokenizers to estimate token inflation,
          cost, latency, and fairness disparities.
        </p>
      </header>

      {modelsLoading && (
        <div className="status-banner">Loading models from backend...</div>
      )}
      {modelsError && (
        <div className="status-banner error">
          Backend connection error: {modelsError}
        </div>
      )}

      <main className="layout">
        <form className="control-stack" onSubmit={handleAnalyze}>
          <TextInputPanel
            text={text}
            onTextChange={setText}
            disabled={modelsLoading || analyzing}
          />
          <ModelSelector
            models={models}
            selectedModelIds={selectedModelIds}
            baselineModelId={baselineModelId}
            onToggleModel={toggleModel}
            onBaselineChange={setBaselineModelId}
            disabled={modelsLoading || analyzing}
          />
          <MetricExplainer />
          <button
            className="analyze-button"
            type="submit"
            disabled={
              modelsLoading ||
              analyzing ||
              models.length === 0 ||
              selectedModelIds.length === 0
            }
          >
            {analyzing ? "Analyzing..." : "Analyze Text"}
          </button>
          <button
            className="leaderboard-button"
            type="button"
            disabled={modelsLoading || leaderboardLoading}
            onClick={handleLoadLeaderboard}
          >
            {leaderboardLoading ? "Loading Leaderboard..." : "View Fairness Leaderboard"}
          </button>
          {analyzeError && <div className="status-banner error">{analyzeError}</div>}
          {leaderboardError && (
            <div className="status-banner error">{leaderboardError}</div>
          )}
        </form>

        <section className="results-panel">
          <h2>Results</h2>
          {!result && (
            <p className="panel-hint">
              Run analysis to view model-by-model tokenization metrics.
            </p>
          )}

          {summary && (
            <section className="results-block">
              <h3>Summary Metrics</h3>
              <div className="metric-grid">
                <MetricCard label="Models analyzed" value={String(summary.modelCount)} />
                <MetricCard label="Baseline model" value={summary.baseline} />
                <MetricCard
                  label="Lowest fairness score"
                  value={`${summary.lowestFairness.toFixed(2)} / 100`}
                />
                <MetricCard
                  label="Highest token multiplier"
                  value={`${summary.highestMultiplier.toFixed(2)}x`}
                />
              </div>
            </section>
          )}

          {result && (
            <section className="results-block">
              <h3>Visual Comparisons</h3>
              <div className="language-badge">
                Language Detected: <strong>{summary?.languageDetected ?? "unknown"}</strong>
              </div>
              <ResultsCharts analyses={result.analyses} />
            </section>
          )}

          {result && (
            <section className="results-block">
              <h3>Detailed Metrics Table</h3>
              <ResultsTable analyses={result.analyses} />
            </section>
          )}

          {showLeaderboard && (
            <section className="results-block">
              <h3>Fairness Leaderboard</h3>
              {leaderboardLoading && (
                <p className="panel-hint">Computing leaderboard from multilingual benchmarks...</p>
              )}
              {leaderboard && (
                <>
                  <p className="panel-hint leaderboard-meta">
                    Languages benchmarked: {leaderboard.languages.join(", ")}
                  </p>
                  <LeaderboardTable rows={leaderboard.leaderboard} />
                </>
              )}
            </section>
          )}
        </section>
      </main>
    </div>
  );
}
