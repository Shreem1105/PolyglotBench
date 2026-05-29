type TextInputPanelProps = {
  text: string;
  disabled?: boolean;
  onTextChange: (value: string) => void;
};

export default function TextInputPanel({ text, disabled = false, onTextChange }: TextInputPanelProps) {
  return (
    <section className="panel panel-input">
      <h2>Text Input</h2>
      <p className="panel-hint">Paste multilingual text to compare tokenizer behavior across selected models.</p>
      <textarea
        className="text-input"
        disabled={disabled}
        value={text}
        onChange={(event) => onTextChange(event.target.value)}
        placeholder="Example: Hello world. नमस्ते दुनिया। こんにちは世界。 مرحبا بالعالم."
      />
      <div className="input-meta">Character count: {text.length}</div>
    </section>
  );
}
