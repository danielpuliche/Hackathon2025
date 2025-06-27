import React, { useState } from 'react';
import './Dashboard.css';

const Dashboard = ({ onBack }) => {
    const [dateRange, setDateRange] = useState('7d');
    const [userType, setUserType] = useState('all');

    // Datos simulados para el desarrollo
    const mockData = {
        categories: [
            { name: 'Admisiones y Matrículas', value: 35, color: '#667eea' },
            { name: 'Información Académica', value: 28, color: '#764ba2' },
            { name: 'Servicios Estudiantiles', value: 15, color: '#48bb78' },
            { name: 'Pagos y Financiación', value: 12, color: '#ed8936' },
            { name: 'Certificados y Documentos', value: 7, color: '#9f7aea' },
            { name: 'Soporte Técnico', value: 3, color: '#e53e3e' }
        ],
        metrics: {
            totalConversations: 1247,
            avgDaily: 45,
            satisfaction: 4.2,
            avgResolutionTime: '2.3 min'
        },
        conversationStatus: [
            { name: 'Resueltos', value: 687, percentage: 55, color: '#48bb78' },
            { name: 'Pendientes', value: 312, percentage: 25, color: '#ed8936' },
            { name: 'En Proceso', value: 186, percentage: 15, color: '#667eea' },
            { name: 'Escalados', value: 62, percentage: 5, color: '#e53e3e' }
        ]
    };

    // Función para renderizar el gráfico de torta simple
    const renderPieChart = () => {
        const total = mockData.categories.reduce((sum, cat) => sum + cat.value, 0);
        let cumulativePercentage = 0;

        return (
            <div className="pie-chart">
                <svg viewBox="0 0 42 42" className="pie-svg">
                    {mockData.categories.map((category, index) => {
                        const percentage = (category.value / total) * 100;
                        const strokeDasharray = `${percentage} ${100 - percentage}`;
                        const strokeDashoffset = -cumulativePercentage;
                        cumulativePercentage += percentage;

                        return (
                            <circle
                                key={index}
                                className="pie-slice"
                                cx="21"
                                cy="21"
                                r="15.915"
                                fill="transparent"
                                stroke={category.color}
                                strokeWidth="3"
                                strokeDasharray={strokeDasharray}
                                strokeDashoffset={strokeDashoffset}
                                transform="rotate(-90 21 21)"
                            />
                        );
                    })}
                </svg>
                <div className="pie-center">
                    <span className="pie-total">{total}</span>
                    <span className="pie-label">Total</span>
                </div>
            </div>
        );
    };

    // Función para renderizar el gráfico de estado de conversaciones
    const renderStatusChart = () => {
        const maxValue = Math.max(...mockData.conversationStatus.map(item => item.value));

        return (
            <div className="status-chart">
                {mockData.conversationStatus.map((status, index) => (
                    <div key={index} className="status-bar-container">
                        <div className="status-info">
                            <span className="status-name">{status.name}</span>
                            <span className="status-count">{status.value}</span>
                        </div>
                        <div className="status-bar-wrapper">
                            <div
                                className="status-bar"
                                style={{
                                    width: `${(status.value / maxValue) * 100}%`,
                                    backgroundColor: status.color
                                }}
                            >
                                <span className="status-percentage">{status.percentage}%</span>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        );
    };

    return (
        <div className="dashboard">
            <div className="dashboard-header">
                {onBack && (
                    <button className="back-button" onClick={onBack}>
                        ← Volver al Panel Administrativo
                    </button>
                )}
                <h1>📊 Dashboard de Conversaciones</h1>
                <p>Campus Popayán - Análisis de interacciones del chatbot</p>

                <div className="dashboard-filters">
                    <select
                        value={dateRange}
                        onChange={(e) => setDateRange(e.target.value)}
                        className="filter-select"
                    >
                        <option value="7d">Últimos 7 días</option>
                        <option value="30d">Últimos 30 días</option>
                        <option value="90d">Últimos 3 meses</option>
                    </select>

                    <select
                        value={userType}
                        onChange={(e) => setUserType(e.target.value)}
                        className="filter-select"
                    >
                        <option value="all">Todos los usuarios</option>
                        <option value="students">Estudiantes</option>
                        <option value="teachers">Docentes</option>
                        <option value="admin">Administrativos</option>
                    </select>
                </div>
            </div>

            <div className="dashboard-metrics">
                <div className="metric-card">
                    <div className="metric-icon">💬</div>
                    <div className="metric-value">{mockData.metrics.totalConversations}</div>
                    <div className="metric-label">Total Conversaciones</div>
                </div>
                <div className="metric-card">
                    <div className="metric-icon">📈</div>
                    <div className="metric-value">{mockData.metrics.avgDaily}</div>
                    <div className="metric-label">Promedio Diario</div>
                </div>
                <div className="metric-card">
                    <div className="metric-icon">⭐</div>
                    <div className="metric-value">{mockData.metrics.satisfaction}</div>
                    <div className="metric-label">Satisfacción</div>
                </div>
                <div className="metric-card">
                    <div className="metric-icon">⏱️</div>
                    <div className="metric-value">{mockData.metrics.avgResolutionTime}</div>
                    <div className="metric-label">Tiempo Promedio</div>
                </div>
            </div>

            <div className="dashboard-content">
                <div className="chart-section">
                    <h3>Conversaciones por Categoría</h3>
                    <div className="chart-container">
                        {renderPieChart()}
                        <div className="chart-legend">
                            {mockData.categories.map((category, index) => (
                                <div key={index} className="legend-item">
                                    <div
                                        className="legend-color"
                                        style={{ backgroundColor: category.color }}
                                    ></div>
                                    <span className="legend-label">{category.name}</span>
                                    <span className="legend-value">{category.value}%</span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

                <div className="status-section">
                    <h3>Estado de Conversaciones</h3>
                    <div className="status-container">
                        {renderStatusChart()}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
