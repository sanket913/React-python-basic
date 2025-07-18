import React, { useState } from 'react';

function App() {
  const [response, setResponse] = useState('');

  const callPythonScript = async () => {
    try {
      const res = await fetch('http://localhost:5000/run-script');
      const data = await res.json();
      setResponse(data.message);
    } catch (error) {
      console.error(error);
      setResponse('Error calling Python script');
    }
  };

  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <h1>React + Normal Python</h1>
      <button onClick={callPythonScript}>Run Hello Script</button>
      <p>{response}</p>
    </div>
  );
}

export default App;
