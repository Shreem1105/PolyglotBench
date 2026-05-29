export default function MetricExplainer() {
  return (
    <section className="panel metric-explainer">
      <h2>Metric Guide</h2>
      <p className="panel-hint">
        Use this quick guide to interpret tokenizer fairness outcomes in research analysis.
      </p>
      <ul>
        <li>
          <strong>Fertility:</strong> tokens per word for the selected text.
        </li>
        <li>
          <strong>Token multiplier:</strong> token count relative to the baseline model.
        </li>
        <li>
          <strong>Estimated attention cost:</strong> token multiplier squared.
        </li>
        <li>
          <strong>Estimated latency:</strong> proxy estimate based on token inflation.
        </li>
        <li>
          <strong>Fairness score:</strong> 0-100 score where less token inflation is better.
        </li>
      </ul>
    </section>
  );
}
