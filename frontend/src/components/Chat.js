import React, { useState } from 'react';
import './Chat.css';
import axios from 'axios';

const Chat = () => {
  const [query, setQuery] = useState('');
  const [botResponse, setBotResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const doctorImage = loading ? './ChatGPT Image May 27, 2025, 07_22_19 PM.png' : './vs8pe84nu1qtbkaexnsltrg5gle0.png';
  const responseImage = loading ? './dots-512.webp' : '';

  const handleSend = async () => {
    if (!query.trim()) return;

    setQuery('');
    setLoading(true);
    setBotResponse('');

    try {
      const res = await axios.post('http://localhost:8000/rag', {
        query,
        chunks: []
      });

      const responseText = 
            typeof res.data === 'string' ? res.data : JSON.stringify(res.data);

      setBotResponse(responseText);
    } catch (err) {
      setBotResponse('Sorry, there was an error.')
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="background-image">
    <strong className="title-style">🩺 Medical Chatbot</strong>
  <div className="chat-container">

    {botResponse.trim() != '' && (
    <div className="chat-window">
        <div className="message bot">
            {botResponse}
        </div>
    </ div>
      )}

    <div className="input-area">
      <textarea
        rows={2}
        placeholder="Describe your symptoms or ask a question..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button onClick={handleSend} disabled={loading}>
        {loading ? '...' : 'Send'}
      </button>
    </div>

    <img
      src={doctorImage}
      alt="Doctor"
      style={{
        position: 'absolute',
        left: '200px',
        top: '250px',
        height: '300px',
        objectFit: 'contain',
        display: 'block',
        margin: '0 auto 1rem auto'
      }}
    />

    {responseImage && (
    <img
        src={responseImage}
        alt="Response"
        style={{
        position: 'absolute',
        left: '470px',
        top: '250px',
        height: '200px',
        width: '100px',
        objectFit: 'contain',
        display: 'block',
        margin: '0 auto 1rem auto'
        }}
    />
    )}

  </div>
</div>

  );
};

export default Chat;
