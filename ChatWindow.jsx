import { useState } from "react";
import MessageBubble from "./MessageBubble";
import SuggestionsPanel from "./SuggestionsPanel";
import EmergencyPanel from "./EmergencyPanel";

function ChatWindow() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [response, setResponse] = useState(null);

  const sendMessage = async () => {
    const res = await fetch("http://localhost:5000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: input })
    });
    const data = await res.json();
    setResponse(data);

    setMessages([...messages, { text: input, sender: "user" }]);

    if (!data.emergency)
      setMessages(m => [...m, { text: data.reply, sender: "bot" }]);

    setInput("");
  };

  return (
    <div>
      {messages.map((m, i) => (
        <MessageBubble key={i} text={m.text} sender={m.sender} />
      ))}

      {response?.emergency && <EmergencyPanel data={response} />}
      {response && !response.emergency && (
        <SuggestionsPanel tips={response.suggestions} />
      )}

      <textarea value={input} onChange={e => setInput(e.target.value)} />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}

export default ChatWindow;