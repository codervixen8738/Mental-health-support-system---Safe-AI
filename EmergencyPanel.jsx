function EmergencyPanel({ data }) {
  return (
    <div className="emergency">
      <h2>🚨 Emergency Support</h2>
      <p>{data.message}</p>
      <div className="hotlines">
        <button onClick={() => window.open('tel:988')}>
          📞 Crisis Lifeline: 988
        </button>
        <button onClick={() => window.open('tel:911')}>
          🚨 Emergency: 911
        </button>
      </div>
    </div>
  );
}

export default EmergencyPanel;