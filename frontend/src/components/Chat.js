import React, { useState, useEffect } from 'react';
import './Chat.css';
import axios from 'axios';

// Fixed set of suggested questions
const Questions = [
  "I’ve had intermittent chest tightness, shortness of breath when climbing stairs, and mild sweating for the past two days.",
  "How should type 2 diabetes be managed in an elderly patient with chronic kidney disease?",
  "I feel dizzy and lightheaded every time I stand up quickly, especially in the morning.",
  "What is the mechanism by which ACE inhibitors lower blood pressure?"
];

const Chat = () => {
  const [query, setQuery] = useState('');
  const [botResponse, setBotResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [suggestedQuestions, setSuggestedQuestions] = useState(Questions);
  const [fullResponse, setFullResponse] = useState(null);
  const doctorImage = loading ? './ChatGPT Image May 27, 2025, 07_22_19 PM.png' : './vs8pe84nu1qtbkaexnsltrg5gle0.png';

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

      const responseText = typeof res.data === 'string'
        ? res.data
        : res.data.answer || 'No answer found!';

      setFullResponse(res.data);
      setBotResponse(responseText);
    } catch (err) {
      setBotResponse('Sorry, there was an error.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="background-image">
      <strong className="title-style">🩺 Dr. Dialogue 🩺</strong>
      <div className="chat-container">
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
      </div>

      <div className="suggestions-grid">
        {suggestedQuestions.map((q, i) => (
          <div
            key={i}
            className="suggested-question"
            onClick={() => setQuery(q)}
          >
            {q}
          </div>
        ))}
      </div>

      {botResponse.trim() !== '' && (
        <div className="chat-window">
          <div className="message bot">{botResponse}</div>
        </div>
      )}

      {loading && <div className="spinner"></div>}

      <img
        src={doctorImage}
        alt="Doctor"
        className='doctor-avatar'
      />

      {loading === false && fullResponse && (
        <div className="response-log">
          <h3>🔍 Metrics</h3>
          <pre>
            {JSON.stringify(
              Object.fromEntries(
                Object.entries(fullResponse).filter(([key]) => key !== 'answer')
              ),
              null,
              2
            )}
          </pre>
        </div>
      )}
    </div>
  );
};

export default Chat;