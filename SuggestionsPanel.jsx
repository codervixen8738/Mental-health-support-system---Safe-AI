function SuggestionsPanel({ tips }) {
  return (
    <div className="suggestions">
      <h3>💡 Helpful Tips</h3>
      {tips?.map((tip, i) => (
        <p key={i}>{tip}</p>
      ))}
    </div>
  );
}

export default SuggestionsPanel;