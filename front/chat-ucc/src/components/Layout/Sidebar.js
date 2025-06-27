import React from 'react';
import './Sidebar.css';
import logo from '../../assets/logos/logo.png';

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
            label: 'Asistente Virtual Personalizado',
            description: 'Chatbot con información institucional'
        },
        {
            id: 'admin',
            icon: '📊',
            label: 'Gestión Administrativa',
            description: 'Herramientas para administradores'
        },
        {
            id: 'consulting',
            icon: '💡',
            label: 'Consultoría',
            description: 'Servicios de asesoría especializada'
        }
    ];

    return (
        <div className="sidebar">
            <div className="sidebar-header">
                <div className="logo">
                    <div className="logo-icon">
                        <img src={logo} alt="Impulsa EDU-Tech" className="logo-image" />
                    </div>
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
        </div>
    );
};

export default Sidebar;
