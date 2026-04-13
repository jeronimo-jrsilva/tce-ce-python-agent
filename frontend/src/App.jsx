import { useState, useEffect, useRef } from 'react';
import Markdown from 'markdown-to-jsx';
import { Send, Bot, User, Trash2, Cpu, ExternalLink, Sun, Moon } from 'lucide-react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [theme, setTheme] = useState(localStorage.getItem('theme') || 'light');
  const [sessionId] = useState(() => 'session-' + Math.random().toString(36).substring(7));
  const chatEndRef = useRef(null);

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }, [theme]);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMsg = { text: input, sender: 'human', id: Date.now() };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/messages', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input, session_id: sessionId })
      });

      if (!response.ok) throw new Error('Falha na comunicação com a API');

      const data = await response.json();
      const aiMsg = { 
        text: data.answer, 
        sources: data.sources || [], 
        sender: 'ai', 
        id: Date.now() + 1 
      };
      setMessages(prev => [...prev, aiMsg]);
    } catch (err) {
      setMessages(prev => [...prev, { 
        text: '⚠️ **Erro ao conectar com o Agente:** ' + err.message, 
        sender: 'ai', 
        isError: true,
        id: Date.now() + 1 
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <Cpu color="#1a73e8" size={32} />
          <div>
            <h1>TCE-CE: Agente de IA Técnico</h1>
            <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
               <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', fontWeight: 500 }}>Sessão Ativa: {sessionId}</span>
               <a href="http://localhost:8000/debug" target="_blank" rel="noreferrer" style={{ fontSize: '0.7rem', color: '#1a73e8', textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '0.2rem' }}>
                 <ExternalLink size={10} /> Lab de Debug
               </a>
            </div>
          </div>
        </div>
        
        <div style={{ marginLeft: 'auto', display: 'flex', gap: '0.75rem' }}>
          <button onClick={toggleTheme} className="theme-toggle" title="Alternar Tema">
            {theme === 'light' ? <Moon size={20} /> : <Sun size={20} />}
          </button>
          
          <button 
            onClick={() => setMessages([])} 
            className="theme-toggle"
            style={{ width: 'auto', padding: '0 0.75rem', display: 'flex', gap: '0.4rem', fontSize: '0.85rem' }}
            title="Limpar Conversa"
          >
            <Trash2 size={16} /> <span className="desktop-only">Limpar</span>
          </button>
        </div>
      </header>

      <div className="chat-window">
        {messages.length === 0 && (
          <div style={{ textAlign: 'center', marginTop: '6rem', maxWidth: '600px', alignSelf: 'center' }}>
            <div style={{ background: theme === 'light' ? '#e8f0fe' : '#303134', width: '80px', height: '80px', borderRadius: '20px', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 1.5rem' }}>
               <Bot size={40} color="#1a73e8" strokeWidth={1.5} />
            </div>
            <h2 style={{ fontSize: '1.5rem', marginBottom: '1rem', color: 'var(--text-main)' }}>Assistente Técnico do TCE-CE</h2>
            <p style={{ color: 'var(--text-secondary)', lineHeight: 1.6 }}>
              Olá! Estou conectado à base de conhecimento técnica oficial. 
              Posso tirar dúvidas sobre **SOLID**, **Composição**, **Herança** e padrões de projeto em Python.
            </p>
            <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', justifyContent: 'center', marginTop: '2rem' }}>
               <button onClick={() => setInput('O que a base diz sobre Herança?')} className="source-tag" style={{ cursor: 'pointer', background: 'var(--bg-container)' }}>O que a base diz sobre Herança?</button>
               <button onClick={() => setInput('Explique Composição em Python.')} className="source-tag" style={{ cursor: 'pointer', background: 'var(--bg-container)' }}>Explique Composição em Python.</button>
               <button onClick={() => setInput('Quais as regras de validação?')} className="source-tag" style={{ cursor: 'pointer', background: 'var(--bg-container)' }}>Quais as regras de validação?</button>
            </div>
          </div>
        )}

        {messages.map(msg => (
          <div key={msg.id} className={`message ${msg.sender} ${msg.isError ? 'error' : ''}`}>
            <div style={{ fontWeight: 600, display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.8rem', fontSize: '0.85rem', opacity: 0.8 }}>
              {msg.sender === 'ai' ? <Bot size={16} /> : <User size={16} />}
              {msg.sender === 'ai' ? 'AGENTE TÉCNICO' : 'VOCÊ'}
            </div>
            
            <div className="markdown-content">
              <Markdown>{msg.text}</Markdown>
            </div>

            {msg.sources && msg.sources.length > 0 && (
              <div className="sources-container">
                <span style={{ fontSize: '0.7rem', fontWeight: 600, width: '100%', marginBottom: '0.4rem', color: 'var(--text-secondary)' }}>FONTES CONSULTADAS NA BASE:</span>
                {msg.sources.map((s, idx) => (
                  <span key={idx} className="source-tag">{s.section}</span>
                ))}
              </div>
            )}
          </div>
        ))}
        
        {loading && (
          <div className="typing-indicator">
            <div className="dot-pulse">
              <div className="dot"></div>
              <div className="dot"></div>
              <div className="dot"></div>
            </div>
            <span>O agente está consultando a base técnica oficial...</span>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      <div className="input-area-container">
        <div className="input-area">
          <input 
            type="text" 
            value={input} 
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Digite sua dúvida técnica aqui..."
            disabled={loading}
            autoFocus
          />
          <button className="send-button" onClick={handleSend} disabled={loading || !input.trim()}>
            <Send size={20} />
          </button>
        </div>
        <p style={{ textAlign: 'center', fontSize: '0.7rem', color: 'var(--text-secondary)', marginTop: '0.75rem' }}>
           Baseado na Documentação Técnica do TCE-CE Agente Challenge v1.0
        </p>
      </div>
    </div>
  );
}

export default App;
