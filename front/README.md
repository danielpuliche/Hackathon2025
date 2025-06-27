# Frontend - Impulsa EDU-Tech
**Universidad Cooperativa de Colombia - Campus Popayán**

## Estructura del Proyecto

El frontend está organizado como una aplicación React moderna con la siguiente estructura:

```
chat-ucc/
├── package.json              # Dependencias y scripts
├── public/                   # Archivos estáticos
│   ├── index.html
│   ├── favicon.ico
│   └── ...
└── src/
    ├── App.js                # Componente principal
    ├── index.js              # Punto de entrada
    ├── components/           # Componentes reutilizables
    │   ├── Chat/
    │   │   ├── ChatWidget.js  # Widget de chat unificado
    │   │   └── ChatWidget.css # Estilos del chat
    │   ├── Dashboard/        # Componentes del dashboard
    │   └── Layout/           # Componentes de layout
    └── styles/               # Estilos globales
        ├── index.css         # Variables CSS y estilos base
        └── App.css           # Estilos de la aplicación
```

## Características del Chat Widget

### ✨ Funcionalidades
- **Chat interactivo** con el backend FastAPI
- **Indicador de escritura** en tiempo real
- **Timestamps** en los mensajes
- **Minimizar/Maximizar** el widget
- **Confirmación de cierre** con opción de conservar historial
- **Detección automática de enlaces** en mensajes
- **Responsive design** para móviles y desktop
- **Paleta de colores corporativa** aplicada

### 🎨 Diseño Visual
- Colores oficiales de Impulsa EDU-Tech
- Animaciones suaves y transiciones
- Iconos y elementos visuales coherentes
- Tipografía optimizada para legibilidad

### 🚀 UX/UI Mejoradas
- Inicio del chat con mensaje de bienvenida
- Chips informativos sobre temas disponibles
- Estados de carga visual
- Soporte para Enter en el input
- Deshabilitación de controles durante loading

## Instalación y Uso

### Prerequisitos
- Node.js 16+ 
- npm o yarn

### Instalación
```bash
cd front/chat-ucc
npm install
```

### Desarrollo
```bash
npm start
```
La aplicación se abrirá en `http://localhost:3000`

### Construcción para Producción
```bash
npm run build
```

### Testing
```bash
npm test
```

## Configuración

### Variables de Entorno
El chat se conecta automáticamente al backend en:
- **API Endpoint**: `http://localhost:8000/ask`
- **Theme Endpoint**: `http://localhost:8000/theme`

### Paleta de Colores
Los colores están definidos en `src/styles/index.css`:
```css
--color-primary: #0A4D68;        /* Azul petróleo */
--color-secondary: #00A8A8;      /* Verde azulado */
--color-background: #F5F7FA;     /* Gris claro */
--color-emphasis: #FF6B6B;       /* Coral */
```

## Integración con Backend

El chat se comunica con el backend a través de:

### Endpoint `/ask`
```javascript
POST http://localhost:8000/ask
{
  "question": "¿Cuáles son los programas disponibles?",
  "conversation_id": "web-chat-123456789"
}
```

### Respuesta
```javascript
{
  "answer": "Los programas disponibles son...",
  "conversation_id": "web-chat-123456789",
  "topic_detected": "programas"
}
```

## Componentes Principales

### ChatWidget
Componente principal del chat que maneja:
- Estados del chat (minimizado, abierto, cerrado)
- Envío y recepción de mensajes
- Integración con el backend
- UX y animaciones

### App
Componente raíz que incluye:
- Dashboard principal
- Navegación entre secciones
- Integración del ChatWidget

## Personalización

### Modificar Colores
Edita las variables CSS en `src/styles/index.css`

### Agregar Funcionalidades al Chat
Modifica `src/components/Chat/ChatWidget.js`

### Cambiar Estilos del Chat
Edita `src/components/Chat/ChatWidget.css`

## Mantenimiento

### Estructura Limpia
- Se eliminaron archivos duplicados
- Un solo componente de chat unificado
- Estilos organizados por componente
- Variables CSS centralizadas

### Buenas Prácticas
- Componentes funcionales con hooks
- Manejo de errores
- Estados de loading
- Accesibilidad básica
- Responsive design

---

## Próximas Mejoras
- [ ] Persistencia de conversaciones
- [ ] Soporte para archivos adjuntos
- [ ] Notificaciones push
- [ ] Temas personalizables
- [ ] Internacionalización

**Desarrollado con ❤️ para Impulsa EDU-Tech - UCC Popayán**
