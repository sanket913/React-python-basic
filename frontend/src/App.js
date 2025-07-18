import React, { useState, useEffect, useRef } from 'react';
import './App.css';

function App() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]); // [{ sender: 'user' | 'bot', text: '' }]
  const messagesEndRef = useRef(null);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = { sender: 'user', text: input };
    setMessages(prev => [...prev, userMsg]);

    try {
      const res = await fetch('https://react-python-basic.onrender.com/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input }),
      });

      const data = await res.json();
      const botMsg = { sender: 'bot', text: data.reply };
      setMessages(prev => [...prev, botMsg]);
    } catch (err) {
      setMessages(prev => [...prev, { sender: 'bot', text: 'Server error.' }]);
    }

    setInput('');
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') sendMessage();
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="chat-app">
      <div className="chat-header">WhatsApp Chat UI</div>

      <div className="chat-body">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`chat-bubble ${msg.sender === 'user' ? 'user' : 'bot'}`}
          >
            {msg.text}
          </div>
        ))}
        <div ref={messagesEndRef}></div>
      </div>

      <div className="chat-input">
        <input
          type="text"
          placeholder="Type a message"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}

export default App;
