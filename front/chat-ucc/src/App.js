import React, { useState } from 'react';
import { Sidebar, ChatWidget, Dashboard } from './components';
import './styles/App.css';

function App() {
    const [activeSection, setActiveSection] = useState('overview');
    const [adminSubSection, setAdminSubSection] = useState(null);

    const handleSectionChange = (section) => {
        setActiveSection(section);
        setAdminSubSection(null); // Reset sub-section when changing main section
    };

    // Función para generar enlace de WhatsApp
    const getWhatsAppLink = () => {
        const phoneNumber = "573122144541";
        const message = `Hola! 👋 
        
Estoy interesado en los servicios de consultoría EDU-Tech de Impulsa para la Universidad Cooperativa de Colombia.

Me gustaría conocer más sobre:
• Optimización de plataformas educativas
• Mejora de atención estudiantil
• Análisis de datos educativos

¿Podríamos agendar una consulta personalizada?

Saludos!`;

        return `https://wa.me/${phoneNumber}?text=${encodeURIComponent(message)}`;
    };

    const renderContent = () => {
        switch (activeSection) {
            case 'overview':
                return (
                    <div className="content-section">
                        <div className="hero-section">
                            <h1>Bienvenido a Impulsa EDU-Tech</h1>
                            <p className="hero-subtitle">Transformando la educación superior con tecnología innovadora</p>

                            <div className="services-grid">
                                <div className="service-card" onClick={() => setActiveSection('chatbot')}>
                                    <div className="service-icon">🤖</div>
                                    <h3>Chatbot Personalizado</h3>
                                    <p>Asistente virtual inteligente con información específica de la UCC para resolver consultas estudiantiles 24/7</p>
                                    <span className="service-cta">Explorar →</span>
                                </div>

                                <div className="service-card" onClick={() => setActiveSection('admin')}>
                                    <div className="service-icon">📊</div>
                                    <h3>Gestión Administrativa</h3>
                                    <p>Interface completa para administradores: gestión de conversaciones, análisis de solicitudes y reportes</p>
                                    <span className="service-cta">Gestionar →</span>
                                </div>

                                <div className="service-card" onClick={() => setActiveSection('consulting')}>
                                    <div className="service-icon">💡</div>
                                    <h3>Consultoría Especializada</h3>
                                    <p>Asesoría experta para optimizar plataformas educativas, mejorar tiempos de respuesta y satisfacción</p>
                                    <span className="service-cta">Consultar →</span>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            case 'chatbot':
                return (
                    <div className="content-section">
                        <h1>🤖 Chatbot Personalizado UCC</h1>
                        <p>Asistente virtual inteligente entrenado con información específica de la Universidad Cooperativa de Colombia. Por medio del asistente virtual puedes consultar requisitos de admisión, fechas claves, costos, becas, procesos y más información relevante.</p>
                        <div className="features-list">
                            <div className="feature-item">✅ Información académica actualizada</div>
                            <div className="feature-item">✅ Disponibilidad 24/7 a consultas de comunidades universitarias y externas</div>
                            <div className="feature-item">✅ Integración con sistemas institucionales</div>
                            <div className="feature-item">✅ Clasificación automática de solicitudes</div>
                        </div>

                        <div className="demo-invitation">
                            <h3>🚀 ¡Prueba el ChatBot en Acción!</h3>
                            <p>Haz clic en el botón de chat flotante (💬) en la esquina inferior derecha para explorar las capacidades del asistente virtual. ¡Pregúntale cualquier cosa sobre la Universidad Cooperativa!</p>
                            <div className="demo-arrow">
                                ↘️ <strong>¡Inicia una conversación ahora!</strong>
                            </div>
                        </div>

                        <ChatWidget />
                    </div>
                );
            case 'admin':
                if (adminSubSection === 'dashboard') {
                    return <Dashboard onBack={() => setAdminSubSection(null)} />;
                }
                return (
                    <div className="content-section">
                        <h1>📊 Panel de Gestión Administrativa</h1>
                        <p>Herramientas completas para administradores educativos</p>

                        <div className="admin-modules">
                            <div className="module-card">
                                <h3>💬 Gestión de Conversaciones</h3>
                                <p>Visualizar, analizar y gestionar todas las interacciones del chatbot</p>
                                <button
                                    className="btn-primary"
                                    onClick={() => setAdminSubSection('dashboard')}
                                >
                                    Ver Dashboard
                                </button>
                            </div>

                            <div className="module-card">
                                <h3>📋 Tipos de Solicitudes</h3>
                                <p>Categorizar y priorizar diferentes tipos de consultas estudiantiles</p>
                                <button className="btn-primary">Gestionar Categorías</button>
                            </div>

                            <div className="module-card">
                                <h3>📈 Reportes y Métricas</h3>
                                <p>Análisis detallado de uso, satisfacción y eficiencia</p>
                                <button className="btn-primary">Ver Reportes</button>
                            </div>

                            <div className="module-card">
                                <h3>👥 Gestión de Usuarios</h3>
                                <p>Administrar accesos y permisos del personal</p>
                                <button className="btn-primary">Gestionar Usuarios</button>
                            </div>
                        </div>
                    </div>
                );
            case 'consulting':
                return (
                    <div className="content-section">
                        <h1>� Consultoría EDU-Tech</h1>
                        <p>Servicios especializados para optimizar su infraestructura educativa</p>

                        <div className="consulting-services">
                            <div className="consulting-card">
                                <div className="consulting-icon">⚡</div>
                                <h3>Optimización de Plataformas</h3>
                                <p>Análisis y mejora de sistemas LMS, portales estudiantiles y herramientas digitales existentes</p>
                                <ul>
                                    <li>Auditoría de performance</li>
                                    <li>Optimización de UX/UI</li>
                                    <li>Integración de sistemas</li>
                                </ul>
                            </div>

                            <div className="consulting-card">
                                <div className="consulting-icon">📞</div>
                                <h3>Mejora de Atención</h3>
                                <p>Implementar estrategias de mejora en la atención al estudiantes y la comunidad externa
                                </p>
                                <ul>
                                    <li>Automatización de procesos</li>
                                    <li>Chatbots especializados</li>
                                    <li>Sistemas de tickets inteligentes</li>
                                </ul>
                            </div>

                            <div className="consulting-card">
                                <div className="consulting-icon">📊</div>
                                <h3>Análisis de Datos</h3>
                                <p>Implementación de herramientas de análisis para toma de decisiones basada en datos</p>
                                <ul>
                                    <li>Dashboard ejecutivos</li>
                                    <li>Métricas de satisfacción</li>
                                    <li>Predicción de tendencias</li>
                                </ul>
                            </div>
                        </div>

                        <div className="cta-section">
                            <h3>¿Listo para transformar su institución?</h3>
                            <p>Contáctenos para una consulta personalizada y descubra cómo Impulsa EDU-Tech puede optimizar su infraestructura educativa</p>
                            <a
                                href={getWhatsAppLink()}
                                className="btn-cta"
                                target="_blank"
                                rel="noopener noreferrer"
                            >
                                📱 Solicitar Consulta por WhatsApp
                            </a>
                        </div>
                    </div>
                );
            default:
                return (
                    <div className="content-section">
                        <h1>Bienvenido a Impulsa EDU-Tech</h1>
                        <p>Selecciona una opción del menú lateral</p>
                    </div>
                );
        }
    };

    return (
        <div className="App">
            <Sidebar
                activeSection={activeSection}
                onSectionChange={handleSectionChange}
            />
            <main className="main-content">
                {renderContent()}
            </main>
        </div>
    );
}

export default App;
