
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from styles import get_css

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="AInomaly",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# THEME MANAGEMENT
# ============================================
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

# Botón Toggle en Sidebar (Opcional, o solo en Config)
# Lo pondremos en Configuración como pidió el usuario, pero cargamos el CSS aquí.
st.markdown(get_css(st.session_state.theme), unsafe_allow_html=True)

# Helper para colores de gráficos según tema
def get_chart_colors():
    if st.session_state.theme == "dark":
        return {
            "text": "#ffffff",
            "grid": "rgba(255,255,255,0.1)",
            "line": "#ffde59",
            "marker_border": "#ffde59",
            "pie_colors": ['rgba(255,255,255,0.2)', '#1800ad', '#ffde59']
        }
    else:
        return {
            "text": "#020617",
            "grid": "rgba(0,0,0,0.1)",
            "line": "#1800ad",
            "marker_border": "#1800ad",
            "pie_colors": ['#cbd5e1', '#1800ad', '#fbbf24']
        }

chart_colors = get_chart_colors()

# ============================================
# COMPONENT HELPERS
# ============================================
def card(title, value, subtext=None):
    st.markdown(f"""
    <div class="custom-card">
        <div class="card-title">{title}</div>
        <div class="card-value">{value}</div>
        {f'<div style="color: var(--text-secondary); font-size: 0.8rem; margin-top: 5px;">{subtext}</div>' if subtext else ''}
    </div>
    """, unsafe_allow_html=True)

def folder_card(name, items_count):
    st.markdown(f"""
    <div class="folder-container">
        <div class="folder-icon">📁</div>
        <div style="font-weight: 500; color: var(--text-primary);">{name}</div>
        <div style="font-size: 0.8rem; color: var(--text-secondary);">{items_count} archivos</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    st.markdown("### 🛡️ AINOMALY", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Navigation
    menu = st.radio(
        "MENU PRICIPAL",
        ["Dashboard", "Grabaciones", "Archivos", "Test Cámara", "Configuración"],
        label_visibility="collapsed"
    )
    
    st.markdown("<div style='flex-grow: 1;'></div>", unsafe_allow_html=True)
    
    # Status Indicator
    st.markdown("---")
    st.caption("Estado Sistema")
    st.markdown("🟢 **En Línea** — v3.1")

# ============================================
# MAIN CONTENT
# ============================================

# Header
st.title(menu)

if menu == "Dashboard":
    # 3-Column Metrics
    c1, c2, c3 = st.columns(3)
    with c1: card("Alertas Hoy", "0", "Sin incidentes recientes")
    with c2: card("Tiempo Activo", "4h 12m", "Monitoreo continuo")
    with c3: card("Cámaras", "1 / 4", "3 desconectadas")
    
    # Modern Charts using Plotly Graph Objects for more control
    st.markdown("### Resumen Mensual")
    
    # Dummy Data creation
    dates = pd.date_range(start="2024-05-01", periods=15)
    values = [2, 1, 5, 3, 8, 4, 2, 1, 0, 3, 2, 6, 4, 8, 3] # Minimalist data
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, 
        y=values, 
        mode='lines+markers',
        line=dict(color=chart_colors['line'], width=3, shape='spline'), 
        marker=dict(size=8, color=chart_colors['line'] if st.session_state.theme=="light" else '#1800ad', line=dict(color=chart_colors['marker_border'], width=2)) 
        # In Light mode: Indigo line, Indigo dots. Dark Mode: Yellow line, Indigo dots with Yellow border.
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=chart_colors['text'], family='Inter'),
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(showgrid=False, tickfont=dict(color=chart_colors['text'])),
        yaxis=dict(showgrid=True, gridcolor=chart_colors['grid'], tickfont=dict(color=chart_colors['text']))
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed Analysis Row
    c_graph1, c_graph2 = st.columns([1, 1])
    with c_graph1:
        st.markdown("#### Distribución de Eventos")
        # Donut Chart
        labels = ['Falsos', 'Caídas', 'Tropiezos']
        values_pie = [15, 55, 30]
        
        fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values_pie, hole=.7)])
        fig_pie.update_traces(
            hoverinfo='label+percent', 
            textinfo='none',
            # Dynamic Colors
            marker=dict(colors=chart_colors['pie_colors'])
        )
        fig_pie.update_layout(
            showlegend=True,
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#a1a1aa'),
            margin=dict(t=0, b=0, l=0, r=0)
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with c_graph2:
        st.markdown("#### Bitácora Reciente")
        
        # HTML Rendering for consistent styling across themes
        st.markdown("""
        <table class="styled-table">
            <thead>
                <tr>
                    <th>Hora</th>
                    <th>Evento</th>
                    <th>Nivel</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>14:02</td>
                    <td>Movimiento Detectado</td>
                    <td><span class="status-badge bg-info">INFO</span></td>
                </tr>
                <tr>
                    <td>11:30</td>
                    <td>Persona Identificada (Admin)</td>
                    <td><span class="status-badge bg-info">INFO</span></td>
                </tr>
                <tr>
                    <td>09:15</td>
                    <td>Sistema Iniciado</td>
                    <td><span class="status-badge bg-success">SUCCESS</span></td>
                </tr>
            </tbody>
        </table>
        """, unsafe_allow_html=True)

elif menu == "Grabaciones":
    # Grid of beautiful cards
    col1, col2, col3 = st.columns(3)
    
    thumbnails = [
        "https://images.unsplash.com/photo-1516733968668-dbdce39c4651?auto=format&fit=crop&w=400&q=80",
        "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=400&q=80",
        "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&w=400&q=80"
    ]
    
    for i in range(9):
        with [col1, col2, col3][i % 3]:
            st.markdown(f"""
            <div class="video-card">
                <div class="rec-indicator">● REC</div>
                <img src="{thumbnails[i % 3]}" />
            </div>
            <div style="display: flex; justify-content: space-between; margin-top: 5px; margin-bottom: 20px;">
                <span style="font-family: 'JetBrains Mono'; font-size: 0.8rem; color: #a1a1aa;">CAM-0{i+1}</span>
                <span style="font-family: 'JetBrains Mono'; font-size: 0.8rem; color: #a1a1aa;">17/05 • 14:3{i}</span>
            </div>
            """, unsafe_allow_html=True)

elif menu == "Archivos":
    c1, c2, c3, c4 = st.columns(4)
    folders = ["Rec_2024", "Incidentes", "Logs", "Sistema", "Backup", "Temp", "Export", "Trash"]
    
    for i, folder in enumerate(folders):
        with [c1, c2, c3, c4][i % 4]:
            folder_card(folder, f"{12 + i*3} items")
            st.markdown("<br>", unsafe_allow_html=True)

elif menu == "Test Cámara":
    
    col_video, col_ctrl = st.columns([3, 1])
    
    with col_video:
        st.markdown("""
        <div style="position: relative; border-radius: 12px; overflow: hidden; border: 1px solid #3f3f46;">
             <div style="position: absolute; width: 100%; height: 100%; 
                background: linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px) 0 0 / 25% 100%, 
                            linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px) 0 0 / 100% 25%;
                pointer-events: none;"></div>
             <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1200&q=80" style="width: 100%; display: block;" />
        </div>
        """, unsafe_allow_html=True)
        
    with col_ctrl:
        st.markdown(f"""
        <div class="custom-card">
            <div class="card-title">Controles</div>
            <div style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 15px;">
                Ajusta los parámetros de detección en tiempo real.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.slider("Sensibilidad", 0, 100, 75)
        st.slider("Umbral Caída", 0.0, 1.0, 0.6)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("Calibrar Fondo", type="primary", use_container_width=True)
        st.button("Reiniciar", use_container_width=True)

elif menu == "Configuración":
    st.markdown("#### Preferencias del Sistema")
    
    t1, t2 = st.tabs(["General", "Seguridad"])
    
    with t1:
        st.text_input("Nombre del Sitio", "Almacén Central")
        st.selectbox("Idioma", ["Español", "English"])
        
        st.markdown("### Apariencia")
        
        # Theme Toggle
        current_theme = st.session_state.theme
        is_dark = current_theme == "dark"
        
        c_toggle, c_lbl = st.columns([0.1, 0.9])
        with c_toggle:
            # Simple button that toggles state
            if st.button("🌙" if is_dark else "☀️", help="Cambiar Tema"):
                st.session_state.theme = "light" if is_dark else "dark"
                st.rerun()
        with c_lbl:
            st.write(f"Modo Actual: **{current_theme.capitalize()}**")
        
    with t2:
        st.text_input("API Key (Telegram)", type="password")
        st.button("Guardar Cambios", type="primary")

