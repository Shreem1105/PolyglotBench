const EXAMPLES = [
  {
    label: "English example",
    text: "Artificial intelligence is changing how people build software.",
  },
  {
    label: "Hindi example",
    text: "कृत्रिम बुद्धिमत्ता सॉफ्टवेयर बनाने के तरीके को बदल रही है।",
  },
  {
    label: "Arabic example",
    text: "الذكاء الاصطناعي يغير طريقة بناء البرمجيات.",
  },
];

type TextInputPanelProps = {
  text: string;
  disabled?: boolean;
  onTextChange: (value: string) => void;
};

export default function TextInputPanel({
  text,
  disabled = false,
  onTextChange,
}: TextInputPanelProps) {
  return (
    <section className="panel panel-input">
      <h2>Text Input</h2>
      <p className="panel-hint">
        Paste multilingual text to compare tokenizer behavior across selected models.
      </p>
      <textarea
        className="text-input"
        disabled={disabled}
        value={text}
        onChange={(event) => onTextChange(event.target.value)}
        placeholder="Example: Hello world. नमस्ते दुनिया। مرحبا بالعالم."
      />
      <div className="input-meta">Character count: {text.length}</div>
      <div className="example-group" aria-label="Quick multilingual examples">
        {EXAMPLES.map((example) => (
          <button
            key={example.label}
            type="button"
            className="example-button"
            disabled={disabled}
            onClick={() => onTextChange(example.text)}
          >
            {example.label}
          </button>
        ))}
      </div>
    </section>
  );
}
