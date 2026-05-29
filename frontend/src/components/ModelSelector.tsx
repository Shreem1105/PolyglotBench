import type { ModelInfo } from "../types/api";

type ModelSelectorProps = {
  models: ModelInfo[];
  selectedModelIds: string[];
  baselineModelId: string;
  disabled?: boolean;
  onToggleModel: (modelId: string) => void;
  onBaselineChange: (modelId: string) => void;
};

export default function ModelSelector({
  models,
  selectedModelIds,
  baselineModelId,
  disabled = false,
  onToggleModel,
  onBaselineChange,
}: ModelSelectorProps) {
  return (
    <section className="panel panel-models">
      <h2>Model Selection</h2>
      <p className="panel-hint">Choose one or more models and set a baseline for multiplier comparisons.</p>

      <div className="model-list">
        {models.map((model) => {
          const checked = selectedModelIds.includes(model.id);
          return (
            <label key={model.id} className="model-item">
              <input
                type="checkbox"
                disabled={disabled}
                checked={checked}
                onChange={() => onToggleModel(model.id)}
              />
              <span className="model-name">{model.display_name}</span>
              <span className="model-provider">{model.provider}</span>
            </label>
          );
        })}
      </div>

      <label className="baseline-select">
        <span>Baseline Model</span>
        <select
          disabled={disabled}
          value={baselineModelId}
          onChange={(event) => onBaselineChange(event.target.value)}
        >
          {models.map((model) => (
            <option key={model.id} value={model.id}>
              {model.display_name}
            </option>
          ))}
        </select>
      </label>
    </section>
  );
}
