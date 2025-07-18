import React, { useState } from 'react';

function App() {
  const [message, setMessage] = useState('');
  const [reply, setReply] = useState('');

  const handleSend = async () => {
    if (!message.trim()) return;

    try {
      const res = await fetch('https://react-python-basic.onrender.com/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      });

      const data = await res.json();
      setReply(data.reply);
    } catch (error) {
      console.error('Error:', error);
      setReply('Error connecting to the bot.');
    }
  };

  return (
    <div style={{ padding: '30px', textAlign: 'center' }}>
      <h2>React + Python Chat</h2>
      <input
        style={{ padding: '10px', width: '300px' }}
        type="text"
        placeholder="Type your message..."
        value={message}
        onChange={(e) => setMessage(e.target.value)}
      />
      <br /><br />
      <button onClick={handleSend} style={{ padding: '10px 20px' }}>
        Send
      </button>
      <br /><br />
      {reply && (
        <div style={{ border: '1px solid #ccc', padding: '15px', width: '300px', margin: '0 auto' }}>
          <strong>Bot:</strong> {reply}
        </div>
      )}
    </div>
  );
}

export default App;
