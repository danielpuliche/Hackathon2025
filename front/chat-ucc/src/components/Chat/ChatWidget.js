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
    const [needsUserType, setNeedsUserType] = useState(false);
    const [userType, setUserType] = useState(null);
    const [userOptions, setUserOptions] = useState([]);
    const [showLanguageSelector, setShowLanguageSelector] = useState(false);
    const [selectedLanguage, setSelectedLanguage] = useState('español');
    const messagesEndRef = useRef(null);

    // Opciones de idioma disponibles
    const languageOptions = [
        { code: 'es', name: 'Español', flag: '🇪🇸', available: true },
        { code: 'en', name: 'English', flag: '🇺🇸', available: false },
        { code: 'ny', name: 'Nasa Yuwe', flag: '🏴', available: false }
    ];

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

    // Renderizar selector de idiomas
    const renderLanguageSelector = () => {
        if (!showLanguageSelector) return null;

        return (
            <div className="ucc-language-selector">
                <div className="language-dropdown">
                    <div className="language-header">
                        <h4>Seleccionar idioma</h4>
                        <button
                            className="close-language-selector"
                            onClick={() => setShowLanguageSelector(false)}
                        >
                            ×
                        </button>
                    </div>
                    <div className="language-options">
                        {languageOptions.map((option, index) => (
                            <button
                                key={index}
                                className={`language-option ${option.available ? 'available' : 'disabled'}`}
                                onClick={() => handleLanguageSelection(option)}
                                disabled={!option.available}
                            >
                                <span className="language-flag">{option.flag}</span>
                                <span className="language-name">{option.name}</span>
                                {!option.available &&
                                    <span className="development-badge">En desarrollo</span>
                                }
                                {option.name === selectedLanguage &&
                                    <span className="selected-badge">✓</span>
                                }
                            </button>
                        ))}
                    </div>
                </div>
            </div>
        );
    };

    // Mostrar mensaje de confirmación de cierre dentro del widget
    if (open && showCloseConfirm && !minimized) {
        return (
            <div className="ucc-chat-widget">
                {renderLanguageSelector()}
                <div className="ucc-chat-header">
                    <div className="university-info">
                        <h3>Impulsa EDU-Tech</h3>
                        <p>UCC Popayán</p>
                    </div>
                    <div>
                        <button
                            className="ucc-chat-language"
                            onClick={() => setShowLanguageSelector(!showLanguageSelector)}
                            title="Cambiar idioma"
                        >
                            🌐
                        </button>
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
                                setUserType(null);
                                setNeedsUserType(false);
                                setUserOptions([]);
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

    const startChat = async () => {
        if (!started) {
            setStarted(true);
            setIsLoading(true);

            try {
                const res = await fetch(API_URL, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        question: "",
                        conversation_id: null
                    })
                });

                const data = await res.json();
                setConversationId(data.conversation_id);

                if (data.needs_user_type) {
                    setNeedsUserType(true);
                    setUserOptions(data.user_options || []);
                }

                const welcomeMsg = {
                    sender: 'bot',
                    text: data.answer,
                    timestamp: new Date()
                };
                setMessages([welcomeMsg]);

            } catch (error) {
                console.error('Error iniciando chat:', error);
                const errorMsg = {
                    sender: 'bot',
                    text: 'Error al conectar con el asistente. Por favor, intenta nuevamente.',
                    timestamp: new Date()
                };
                setMessages([errorMsg]);
            } finally {
                setIsLoading(false);
            }
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

    // Renderizar opciones de tipo de usuario
    const renderUserTypeOptions = () => {
        if (!needsUserType || userOptions.length === 0) return null;

        return (
            <div className="ucc-user-type-selection">
                <div className="user-type-buttons">
                    {userOptions.map((option, index) => (
                        <button
                            key={index}
                            className="user-type-button"
                            onClick={() => handleUserTypeSelection(option)}
                            disabled={isLoading}
                        >
                            {option}
                        </button>
                    ))}
                </div>
            </div>
        );
    };

    // Mostrar mensaje de bienvenida con botón para iniciar
    if (open && !started && !minimized) {
        return (
            <div className="ucc-chat-widget">
                {renderLanguageSelector()}
                <div className="ucc-chat-header">
                    <div className="university-info">
                        <h3>Impulsa EDU-Tech</h3>
                        <p>UCC Popayán</p>
                    </div>
                    <div>
                        <button
                            className="ucc-chat-language"
                            onClick={() => setShowLanguageSelector(!showLanguageSelector)}
                            title="Cambiar idioma"
                        >
                            🌐
                        </button>
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
                    conversation_id: conversationId,
                    user_type: userType
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

    const handleUserTypeSelection = async (selectedType) => {
        setUserType(selectedType);
        setNeedsUserType(false);
        setIsLoading(true);

        // Agregar mensaje del usuario
        const userMsg = {
            sender: 'user',
            text: selectedType,
            timestamp: new Date()
        };
        setMessages((msgs) => [...msgs, userMsg]);

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
                    question: selectedType,
                    conversation_id: conversationId,
                    user_type: selectedType
                })
            });

            const data = await res.json();

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
            console.error('Error enviando selección de usuario:', error);
            setMessages((msgs) => [
                ...msgs.slice(0, -1),
                {
                    sender: 'bot',
                    text: 'Error al procesar tu selección. Por favor, intenta nuevamente.',
                    timestamp: new Date()
                }
            ]);
        } finally {
            setIsLoading(false);
        }
    };

    // Función para manejar la selección de idioma
    const handleLanguageSelection = (language) => {
        if (language.available) {
            setSelectedLanguage(language.name);
            setShowLanguageSelector(false);
        } else {
            // Mostrar mensaje de "en desarrollo" para idiomas no disponibles
            const developmentMsg = {
                sender: 'bot',
                text: `El idioma ${language.name} está en desarrollo. Próximamente estará disponible. Por ahora, continuaremos en español.`,
                timestamp: new Date()
            };
            setMessages((msgs) => [...msgs, developmentMsg]);
            setShowLanguageSelector(false);
        }
    };

    // Función para manejar el botón de chat de voz
    const handleVoiceChat = () => {
        const voiceMsg = {
            sender: 'bot',
            text: 'El chat de voz está en desarrollo. Próximamente podrás usar esta funcionalidad para hablar directamente con el asistente virtual.',
            timestamp: new Date()
        };
        setMessages((msgs) => [...msgs, voiceMsg]);
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
            {renderLanguageSelector()}
            <div className="ucc-chat-header">
                <div className="university-info">
                    <h3>Impulsa EDU-Tech</h3>
                    <p>UCC Popayán</p>
                </div>
                <div>
                    <button
                        className="ucc-chat-language"
                        onClick={() => setShowLanguageSelector(!showLanguageSelector)}
                        title="Cambiar idioma"
                    >
                        🌐
                    </button>
                    <button className="ucc-chat-min" onClick={() => setMinimized(true)} title="Minimizar">_</button>
                    <button className="ucc-chat-close" onClick={handleClose} title="Cerrar">&times;</button>
                </div>
            </div>
            <div className="ucc-chat-messages">
                {messages.map((msg, i) => renderMessage(msg, i))}
                {renderUserTypeOptions()}
                <div ref={messagesEndRef} />
            </div>
            <form className="ucc-chat-form" onSubmit={sendMessage}>
                <div className="input-container">
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
                        className="ucc-voice-button"
                        type="button"
                        onClick={handleVoiceChat}
                        title="Chat de voz (en desarrollo)"
                        disabled={isLoading}
                    >
                        🎤
                    </button>
                </div>
                <button
                    className="ucc-chat-send"
                    type="submit"
                    disabled={!input.trim() || isLoading}
                >
                    {isLoading ? '...' : 'Enviar'}
                </button>
            </form>
            {renderLanguageSelector()}
        </div>
    );
}
