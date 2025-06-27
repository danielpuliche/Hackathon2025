import React, { useState, useRef, useEffect } from 'react';
import './ChatWidget.css';

const API_URL = 'http://localhost:8000/ask';
const THEME_URL = 'http://localhost:8000/theme';

export default function ChatWidget() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [open, setOpen] = useState(false);
    const [started, setStarted] = useState(false);
    const [conversationId, setConversationId] = useState(null);
    const [minimized, setMinimized] = useState(false);
    const [showCloseConfirm, setShowCloseConfirm] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);

    // Cargar configuración de tema desde el backend (opcional)
    useEffect(() => {
        fetch(THEME_URL)
            .then(res => res.json())
            .then(data => {
                // Aplicar tema si es necesario
                console.log('Tema cargado:', data.theme);
            })
            .catch(err => console.log('Error cargando tema:', err));
    }, []);

    useEffect(() => {
        if (open && !minimized && messagesEndRef.current) {
            messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
        }
    }, [messages, open, minimized]);

    // Mostrar mensaje de confirmación de cierre dentro del widget
    if (open && showCloseConfirm && !minimized) {
        return (
            <div className="ucc-chat-widget">
                <div className="ucc-chat-header">
                    <div className="university-info">
                        <h3>Impulsa EDU-Tech</h3>
                        <p>UCC Popayán</p>
                    </div>
                    <div>
                        <button className="ucc-chat-min" onClick={() => setMinimized(true)} title="Minimizar">_</button>
                        <button className="ucc-chat-close" onClick={() => setShowCloseConfirm(false)} title="Cancelar">&times;</button>
                    </div>
                </div>
                <div className="ucc-chat-messages">
                    <div className="ucc-close-confirmation">
                        <div className="ucc-close-title">
                            ¿Deseas cerrar la sesión de chat?<br />
                            Se borrará el historial de la conversación.
                        </div>
                        <div className="ucc-close-buttons">
                            <button className="ucc-close-button-confirm" onClick={() => {
                                setStarted(false);
                                setMessages([]);
                                setConversationId(null);
                                setOpen(false);
                                setMinimized(false);
                                setShowCloseConfirm(false);
                            }}>
                                Sí, cerrar
                            </button>
                            <button className="ucc-close-button-cancel" onClick={() => setShowCloseConfirm(false)}>
                                Cancelar
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    // Función para cerrar el chat y mostrar confirmación
    const handleClose = () => {
        if (started) {
            setShowCloseConfirm(true);
        } else {
            setOpen(false);
            setMinimized(false);
        }
    };

    const startChat = () => {
        if (!started) {
            const welcomeMsg = {
                sender: 'bot',
                text: '¡Hola! Soy tu asistente virtual de Impulsa EDU-Tech. ¿En qué puedo ayudarte hoy?',
                timestamp: new Date()
            };
            setMessages([welcomeMsg]);
            setStarted(true);
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage(e);
        }
    };

    function addLinks(text) {
        return text.replace(/(https?:\/\/[^\s]+)/g, url => `<a href="${url}" target="_blank" rel="noopener noreferrer">${url}</a>`);
    }

    const renderMessage = (msg, index) => {
        if (msg.isTyping) {
            return (
                <div key={index} className="ucc-chat-msg bot">
                    <div className="message-bubble typing">
                        <div className="typing-indicator">
                            <span></span>
                            <span></span>
                            <span></span>
                        </div>
                    </div>
                </div>
            );
        }

        return (
            <div key={index} className={`ucc-chat-msg ${msg.sender}`}>
                <div className="message-bubble" dangerouslySetInnerHTML={{ __html: addLinks(msg.text) }} />
                {msg.timestamp && (
                    <div className="message-timestamp">
                        {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </div>
                )}
            </div>
        );
    };

    // Mostrar mensaje de bienvenida con botón para iniciar
    if (open && !started && !minimized) {
        return (
            <div className="ucc-chat-widget">
                <div className="ucc-chat-header">
                    <div className="university-info">
                        <h3>Impulsa EDU-Tech</h3>
                        <p>UCC Popayán</p>
                    </div>
                    <div>
                        <button className="ucc-chat-min" onClick={() => setMinimized(true)} title="Minimizar">_</button>
                        <button className="ucc-chat-close" onClick={handleClose} title="Cerrar">&times;</button>
                    </div>
                </div>
                <div className="ucc-chat-messages">
                    <div className="ucc-welcome-screen">
                        <div className="ucc-welcome-icon">🎓</div>
                        <h4 className="ucc-welcome-title">¡Hola! Soy tu asistente virtual</h4>
                        <p className="ucc-welcome-subtitle">Estoy aquí para ayudarte con información sobre programas, admisiones, biblioteca y becas de la UCC Popayán.</p>
                        <button className="ucc-start-button" onClick={startChat}>
                            Iniciar conversación
                        </button>
                    </div>
                </div>
            </div>
        );
    }

    const sendMessage = async (e) => {
        e.preventDefault();
        if (!input.trim() || isLoading) return;

        // Agregar mensaje del usuario
        const userMsg = {
            sender: 'user',
            text: input,
            timestamp: new Date()
        };

        setMessages((msgs) => [...msgs, userMsg]);
        setInput('');
        setIsLoading(true);
        setStarted(true);

        // Agregar indicador de escritura
        const typingMsg = {
            sender: 'bot',
            text: '',
            isTyping: true
        };
        setMessages((msgs) => [...msgs, typingMsg]);

        try {
            const res = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    question: userMsg.text,
                    conversation_id: conversationId
                })
            });

            const data = await res.json();
            setConversationId(data.conversation_id);

            // Reemplazar indicador de escritura con respuesta
            setMessages((msgs) => [
                ...msgs.slice(0, -1),
                {
                    sender: 'bot',
                    text: data.answer,
                    timestamp: new Date()
                }
            ]);
        } catch (error) {
            console.error('Error enviando mensaje:', error);
            setMessages((msgs) => [
                ...msgs.slice(0, -1),
                {
                    sender: 'bot',
                    text: 'Error al conectar con el asistente. Por favor, intenta nuevamente.',
                    timestamp: new Date()
                }
            ]);
        } finally {
            setIsLoading(false);
        }
    };

    // FAB minimizado
    if (!open || minimized) {
        return (
            <button className="ucc-chat-fab" onClick={() => { setOpen(true); setMinimized(false); }} title="Abrir chat">
                💬
                {started && <span className="ucc-chat-fab-badge" title="Chat activo" />}
            </button>
        );
    }

    // Chat abierto y activo
    return (
        <div className="ucc-chat-widget">
            <div className="ucc-chat-header">
                <div className="university-info">
                    <h3>Impulsa EDU-Tech</h3>
                    <p>UCC Popayán</p>
                </div>
                <div>
                    <button className="ucc-chat-min" onClick={() => setMinimized(true)} title="Minimizar">_</button>
                    <button className="ucc-chat-close" onClick={handleClose} title="Cerrar">&times;</button>
                </div>
            </div>
            <div className="ucc-chat-messages">
                {messages.map((msg, i) => renderMessage(msg, i))}
                <div ref={messagesEndRef} />
            </div>
            <form className="ucc-chat-form" onSubmit={sendMessage}>
                <input
                    className="ucc-chat-input"
                    type="text"
                    placeholder="Escribe tu pregunta..."
                    value={input}
                    onChange={e => setInput(e.target.value)}
                    onKeyPress={handleKeyPress}
                    autoComplete="off"
                    disabled={isLoading}
                    required
                />
                <button
                    className="ucc-chat-send"
                    type="submit"
                    disabled={!input.trim() || isLoading}
                >
                    {isLoading ? '...' : 'Enviar'}
                </button>
            </form>
        </div>
    );
}
