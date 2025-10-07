import React, { useEffect, useState, useRef } from 'react';
import axios from 'axios';

export default function Chat({ user }) {
  const [messages, setMessages] = useState([]);
  const [text, setText] = useState("");
  const messagesEnd = useRef(null);

  const fetchMessages = () => {
    axios.get('/api/chat/messages')
      .then(res => setMessages(res.data));
  };

  useEffect(() => {
    fetchMessages();
    const interval = setInterval(fetchMessages, 3000); // Poll every 3s
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    messagesEnd.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = e => {
    e.preventDefault();
    if (!text.trim()) return;
    axios.post('/api/chat/messages', { text })
      .then(() => {
        setText("");
        fetchMessages();
      });
  };

  return (
    <div style={{
      background: "#23272a", borderRadius: 8, padding: 12, margin: "16px 0", maxWidth: 400
    }}>
      <h4>Team Chat</h4>
      <div style={{
        maxHeight: 180, overflowY: "auto", border: "1px solid #444", marginBottom: 8, padding: "4px 8px", background: "#181a1b"
      }}>
        {messages.map((msg, idx) => (
          <div key={idx} style={{ color: msg.user === user.username ? "#1f8ef1" : "#fff" }}>
            <b>{msg.user}</b> <small>({msg.role})</small>: {msg.text}
            <div style={{ fontSize: "0.7em", color: "#aaa" }}>{msg.timestamp}</div>
          </div>
        ))}
        <div ref={messagesEnd}></div>
      </div>
      <form onSubmit={sendMessage} style={{ display: "flex" }}>
        <input
          value={text}
          onChange={e => setText(e.target.value)}
          placeholder="Type a message"
          style={{ flex: 1 }}
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}