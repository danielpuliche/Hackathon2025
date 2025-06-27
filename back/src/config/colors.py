"""
Constantes de colores y estilos para Impulsa EDU-Tech
Universidad Cooperativa de Colombia - Campus Popayán
"""

# Paleta de colores principal
COLORS = {
    'primary': '#0A4D68',
    'primary_light': '#0F5A7A', 
    'primary_dark': '#083A52',
    
    'secondary': '#00A8A8',
    'secondary_light': '#00BABA',
    'secondary_dark': '#008888',
    
    'background': '#F5F7FA',
    'text': '#1A1A1A',
    'emphasis': '#FF6B6B',
    'success': '#2ECC71',
    
    # Grises complementarios
    'gray_50': '#F9FAFB',
    'gray_100': '#F3F4F6', 
    'gray_200': '#E5E7EB',
    'gray_300': '#D1D5DB',
    'gray_400': '#9CA3AF',
    'gray_500': '#6B7280',
    'gray_600': '#4B5563',
    'gray_700': '#374151',
    'gray_800': '#1F2937',
    'gray_900': '#111827',
}

# Configuración de tema para respuestas del chatbot
CHAT_THEME = {
    'user_message_bg': COLORS['primary'],
    'user_message_text': '#FFFFFF',
    'bot_message_bg': '#FFFFFF',
    'bot_message_text': COLORS['text'],
    'bot_message_accent': COLORS['secondary'],
    'container_bg': COLORS['background'],
    'border_color': COLORS['gray_200']
}

# Estados para notificaciones
STATUS_COLORS = {
    'success': COLORS['success'],
    'warning': COLORS['emphasis'], 
    'info': COLORS['secondary'],
    'error': COLORS['emphasis']
}

# Configuración CSS para inyección dinámica
CSS_VARIABLES = {
    '--color-primary': COLORS['primary'],
    '--color-secondary': COLORS['secondary'],
    '--color-background': COLORS['background'],
    '--color-text': COLORS['text'],
    '--color-emphasis': COLORS['emphasis'],
    '--color-success': COLORS['success']
}

def get_theme_config():
    """Retorna configuración de tema para el frontend"""
    return {
        'colors': COLORS,
        'chat_theme': CHAT_THEME,
        'status_colors': STATUS_COLORS,
        'css_variables': CSS_VARIABLES
    }
