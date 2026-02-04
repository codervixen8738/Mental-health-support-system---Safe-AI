function MessageBubble({ text, sender }) {
  return (
    <div className={`message ${sender}`}>
      <p>{text}</p>
    </div>
  );
}

export default MessageBubble;