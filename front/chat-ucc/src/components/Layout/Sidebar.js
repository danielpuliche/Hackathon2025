import React from 'react';
import './Sidebar.css';

const Sidebar = ({ activeSection, onSectionChange }) => {
    const menuItems = [
        {
            id: 'overview',
            icon: '🏠',
            label: 'Inicio',
            description: 'Vista general de Impulsa EDU-Tech'
        },
        {
            id: 'chatbot',
            icon: '🤖',
            label: 'Chatbot Personalizado',
            description: 'Asistente virtual con información institucional'
        },
        {
            id: 'admin',
            icon: '📊',
            label: 'Gestión Administrativa',
            description: 'Gestionar conversaciones y solicitudes'
        },
        {
            id: 'consulting',
            icon: '�',
            label: 'Consultoría',
            description: 'Asesoría para mejora de plataformas'
        },
        {
            id: 'settings',
            icon: '⚙️',
            label: 'Configuración',
            description: 'Ajustes del sistema'
        }
    ];

    return (
        <div className="sidebar">
            <div className="sidebar-header">
                <div className="logo">
                    <span className="logo-icon">🚀</span>
                    <span className="logo-text">Impulsa EDU-Tech</span>
                </div>
                <div className="logo-subtitle">
                    Plataforma UCC
                </div>
            </div>

            <nav className="sidebar-nav">
                {menuItems.map(item => (
                    <button
                        key={item.id}
                        className={`nav-item ${activeSection === item.id ? 'active' : ''}`}
                        onClick={() => onSectionChange(item.id)}
                        title={item.description}
                    >
                        <span className="nav-icon">{item.icon}</span>
                        <span className="nav-label">{item.label}</span>
                    </button>
                ))}
            </nav>

            <div className="sidebar-footer">
                <div className="user-info">
                    <span className="user-icon">👤</span>
                    <span className="user-name">Administrador</span>
                </div>
            </div>
        </div>
    );
};

export default Sidebar;
