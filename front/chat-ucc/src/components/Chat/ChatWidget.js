import React, { useState, useRef, useEffect } from 'react';
import './ChatWidget.css';

const API_URL = 'http://localhost:8000/ask'; // Cambia si tu backend usa otro puerto

export default function ChatWidget() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [open, setOpen] = useState(false); // inicia minimizado
    const [started, setStarted] = useState(false);
    const [conversationId, setConversationId] = useState(null);
    const [minimized, setMinimized] = useState(false);
    const [showCloseConfirm, setShowCloseConfirm] = useState(false);
    const messagesEndRef = useRef(null);

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
                    Asistente UCC Popayán
                    <div>
                        <button className="ucc-chat-min" onClick={() => setMinimized(true)} title="Minimizar">_</button>
                        <button className="ucc-chat-close" onClick={() => setShowCloseConfirm(false)} title="Cancelar">&times;</button>
                    </div>
                </div>
                <div className="ucc-chat-messages" style={{ textAlign: 'center', display: 'flex', flexDirection: 'column', justifyContent: 'center', height: '100%' }}>
                    <div style={{ margin: 'auto' }}>
                        <div style={{ marginBottom: 16, fontWeight: 'bold' }}>¿Deseas cerrar la sesión de chat?<br />Se borrará el historial.</div>
                        <button className="ucc-chat-send" style={{ marginRight: 8 }} onClick={() => {
                            setStarted(false);
                            setMessages([]);
                            setConversationId(null);
                            setOpen(false);
                            setMinimized(false);
                            setShowCloseConfirm(false);
                        }}>Sí, cerrar</button>
                        <button className="ucc-chat-send" onClick={() => setShowCloseConfirm(false)}>Cancelar</button>
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

    // Mostrar mensaje de bienvenida con botón para iniciar
    if (open && !started && !minimized) {
        return (
            <div className="ucc-chat-widget">
                <div className="ucc-chat-header">
                    Asistente UCC Popayán
                    <div>
                        <button className="ucc-chat-min" onClick={() => setMinimized(true)} title="Minimizar">_</button>
                        <button className="ucc-chat-close" onClick={handleClose} title="Cerrar">&times;</button>
                    </div>
                </div>
                <div className="ucc-chat-messages">
                    <div className="ucc-chat-msg bot">
                        Hola, soy el asistente virtual UCC Popayán y estoy aquí para ayudarte con información sobre programas, admisiones, biblioteca y más.<br />¿Deseas iniciar el chat?
                    </div>
                </div>
                <div style={{ padding: 16, textAlign: 'center' }}>
                    <button className="ucc-chat-send" onClick={() => {
                        setStarted(true);
                        setMessages([
                            { sender: 'bot', text: '¡Chat iniciado! ¿En qué puedo ayudarte?' }
                        ]);
                        setConversationId(crypto.randomUUID());
                    }}>Iniciar chat</button>
                </div>
            </div>
        );
    }

    function addLinks(text) {
        return text.replace(/(https?:\/\/[^\s]+)/g, url => `<a href="${url}" target="_blank" rel="noopener noreferrer">${url}</a>`);
    }

    const sendMessage = async (e) => {
        e.preventDefault();
        if (!input.trim()) return;
        const userMsg = { sender: 'user', text: input };
        setMessages((msgs) => [...msgs, userMsg, { sender: 'bot', text: '<em>Escribiendo...</em>' }]);
        setInput('');
        try {
            const res = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: input, conversation_id: conversationId })
            });
            const data = await res.json();
            setConversationId(data.conversation_id);
            setMessages((msgs) => [
                ...msgs.slice(0, -1),
                { sender: 'bot', text: data.answer }
            ]);
        } catch {
            setMessages((msgs) => [
                ...msgs.slice(0, -1),
                { sender: 'bot', text: 'Error al conectar con el asistente.' }
            ]);
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
                Asistente UCC Popayán
                <div>
                    <button className="ucc-chat-min" onClick={() => setMinimized(true)} title="Minimizar">_</button>
                    <button className="ucc-chat-close" onClick={handleClose} title="Cerrar">&times;</button>
                </div>
            </div>
            <div className="ucc-chat-messages">
                {messages.map((msg, i) => (
                    <div key={i} className={`ucc-chat-msg ${msg.sender}`} dangerouslySetInnerHTML={{ __html: addLinks(msg.text) }} />
                ))}
                <div ref={messagesEndRef} />
            </div>
            <form className="ucc-chat-form" onSubmit={sendMessage}>
                <input
                    className="ucc-chat-input"
                    type="text"
                    placeholder="Escribe tu pregunta..."
                    value={input}
                    onChange={e => setInput(e.target.value)}
                    autoComplete="off"
                    required
                />
                <button className="ucc-chat-send" type="submit">Enviar</button>
            </form>
        </div>
    );
}
