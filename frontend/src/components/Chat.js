import React, { useState, useEffect} from 'react';
import './Chat.css';
import axios from 'axios';


const Questions = [
  "What could be causing a persistent lump under my nipple accompanied by stomach pain?",
  "Why do I experience severe lower back and hip pain upon waking up, which sometimes radiates down my legs?",
  "Is a sudden, painless bump on the leg of a 69-year-old man an emergency, especially if he has a history of triple bypass surgery?",
  "What might be the reason for recurring yeast infections despite treatment?",
  "Could a severe headache with temple pain and numbness in the arm be related to a previous brain aneurysm?",
  "What causes sudden lower right back pain without any apparent injury?",
  "Why do I feel dizzy and lightheaded daily, even though I can perform daily activities?",
  "Is it normal to wake up with arms raised involuntarily, especially after multiple neck and back surgeries?",
  "What could be the reason for numbness and tingling in the legs and arms, along with dizziness and nausea?",
  "Can sciatica pain from a past hip reconstruction lead to facial numbness and cognitive issues?",
  "Is it safe to stop taking spironolactone prescribed for heart problems if the medication runs out?",
  "What are the risks of discontinuing coumadin in a patient with a pacemaker due to side effects like nausea and dizziness?",
  "Can long-term use of cetrizine for skin allergies cause drowsiness, and are there alternative treatments?",
  "Is it common to experience side effects like tiny boils on the forehead after using Minoxidil 5% for male pattern baldness?",
  "What are the implications of high cholesterol and triglyceride levels, and what treatments are recommended?",
  "Is it possible to conceive after gaining weight and experiencing irregular periods post-tuberculosis treatment?",
  "What could cause a 3-month-old baby to have difficulty sleeping unless held, despite no nasal blockage?",
  "Are recurring rashes and hives in a 1-year-9-month-old child, especially after naps, indicative of a milk allergy?",
  "What might cause a 7-year-old child to stop chewing and take deep breaths while eating, and could it be related to nasal blockage?",
  "Is it normal for a 9-month-old baby to develop a rash after introducing solid foods like oatmeal?"
];

function sampleQuestions() {
    const shuffledQuestions = [...Questions].sort(() => 0.5 - Math.random());
    return shuffledQuestions.slice(0,4);
}

const Chat = () => {
  const [query, setQuery] = useState('');
  const [botResponse, setBotResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [suggestedQuestions, setSuggestedQuestions] = useState([]);
  const [fullResponse, setFullResponse] = useState(null);
  const doctorImage = loading ? './ChatGPT Image May 27, 2025, 07_22_19 PM.png' : './vs8pe84nu1qtbkaexnsltrg5gle0.png';
  const responseImage = loading ? '' : '';

  useEffect(() => {
      setSuggestedQuestions(sampleQuestions());
    }, []);

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
            typeof res.data === 'string' ? res.data : res.data.answer || 'No answer found!';

      setFullResponse(res.data);

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

    {botResponse.trim() != '' && (
    <div className="chat-window">
        <div className="message bot">
            {botResponse}
        </div>
    </ div>
      )}

    {loading && (
        <div className="spinner">
        </div>
    )}


    <img
      src={doctorImage}
      alt="Doctor"
      style={{
        position: 'absolute',
        left: '200px',
        top: '350px',
        height: '300px',
        objectFit: 'contain',
        display: 'block',
        margin: '0 auto 1rem auto'
      }}
    />

    {loading != true && fullResponse && (
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
