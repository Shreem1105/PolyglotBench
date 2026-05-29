export type ModelInfo = {
  id: string;
  display_name: string;
  provider: string;
  tokenizer_type: string;
  tokenizer_name: string;
  input_price_per_million_tokens: number;
  notes: string;
};

export type ModelsResponse = {
  models: ModelInfo[];
};

export type AnalyzeRequest = {
  text: string;
  model_ids: string[];
  baseline_model_id?: string | null;
};

export type ModelAnalysis = {
  model_id: string;
  display_name: string;
  provider: string;
  language_detected: string;
  token_count: number;
  word_count: number;
  character_count_no_spaces: number;
  fertility: number;
  token_multiplier: number;
  estimated_attention_cost_multiplier: number;
  estimated_latency_multiplier: number;
  input_cost_estimate_usd: number;
  fairness_score: number;
};

export type AnalyzeResponse = {
  baseline_model_id: string;
  text_preview: string;
  analyses: ModelAnalysis[];
};

export type LeaderboardRow = {
  rank: number;
  model_id: string;
  average_fairness_score: number;
};

export type LeaderboardResponse = {
  languages: string[];
  models: string[];
  baseline_model_id?: string;
  leaderboard: LeaderboardRow[];
};
