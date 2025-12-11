import streamlit as st
import base64

# ============================================
# 1. CONFIGURACIÓN DE PÁGINA
# ============================================
st.set_page_config(
    page_title="AInomaly - Guardián Digital",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# 📍 CONFIGURACIÓN DE IMÁGENES
# ============================================
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

# --- Reemplaza con tus nombres de archivo ---
ruta_hero_bg = "hero_obrero.jpg"
ruta_industria = "industria.jpg"
ruta_hogar = "abuelo.jpg"

# Procesamiento
img_hero_b64 = get_base64_image(ruta_hero_bg)
img_ind_b64 = get_base64_image(ruta_industria)
img_home_b64 = get_base64_image(ruta_hogar)

# Fallbacks (imágenes de internet si no encuentra las locales)
url_hero = f"data:image/jpeg;base64,{img_hero_b64}" if img_hero_b64 else "https://images.unsplash.com/photo-1541888946425-d81bb19240f5?q=80&w=1000&auto=format&fit=crop"
url_ind = f"data:image/jpeg;base64,{img_ind_b64}" if img_ind_b64 else "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&w=800"
url_home = f"data:image/jpeg;base64,{img_home_b64}" if img_home_b64 else "https://images.unsplash.com/photo-1576765608535-5f04d1e3f289?auto=format&fit=crop&w=800"


# ============================================
# 2. ESTILOS CSS (MODO CLARO FORZADO)
# ============================================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    :root {{
        --primary: #000080;
        --accent: #FFD700;
        --text-dark: #1F2937;
        --bg-white: #FFFFFF;
    }}

    /* === FORZAR MODO CLARO (LIGHT MODE) === */
    /* Esto sobreescribe el tema oscuro del sistema */
    [data-testid="stAppViewContainer"] {{
        background-color: white !important;
        color: var(--text-dark) !important;
    }}
    [data-testid="stHeader"] {{
        background-color: rgba(255, 255, 255, 0) !important; /* Header transparente */
    }}
    [data-testid="stSidebar"] {{
        background-color: #f8f9fa !important; 
    }}
    /* Forzar color de textos generales */
    p, span, div, li {{
        color: #374151;
    }}
    /* Forzar inputs para que no se vean oscuros */
    input, textarea, select, div[data-baseweb="select"] {{
        background-color: white !important;
        color: black !important;
        border-color: #e5e7eb !important;
    }}
    /* ========================================= */

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
        scroll-behavior: smooth;
    }}
    
    #MainMenu, footer {{visibility: hidden;}}
    .block-container {{ padding-top: 2rem; }}

    /* NAVBAR */
    .navbar {{
        position: fixed; top: 0; left: 0; width: 100%;
        background: rgba(255, 255, 255, 0.95);
        padding: 1rem 2rem; z-index: 9999;
        display: flex; justify-content: space-between; align-items: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
    }}
    .nav-logo {{ font-size: 1.5rem; font-weight: 700; color: var(--primary); text-decoration: none; }}
    .nav-links {{ display: flex; gap: 2rem; }}
    .nav-link {{ color: #4B5563 !important; text-decoration: none; font-weight: 600; transition: color 0.3s; }}
    .nav-link:hover {{ color: var(--primary) !important; }}
    .nav-cta {{ background: var(--primary); color: white !important; padding: 0.5rem 1.2rem; border-radius: 0.5rem; }}

    /* TARJETAS */
    .custom-card {{
        background: white; padding: 2rem; border-radius: 1rem;
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        height: 100%; transition: transform 0.2s;
    }}
    .custom-card:hover {{ transform: translateY(-5px); border-color: #BFDBFE; }}

    .icon-box {{
        width: 3rem; height: 3rem; background: #FEF9C3; color: var(--primary);
        border-radius: 0.5rem; display: flex; align-items: center; justify-content: center;
        font-size: 1.5rem; margin-bottom: 1rem;
    }}

    /* BARRA ESTADISTICAS */
    .stats-bar {{
        background: var(--primary); color: white; padding: 2rem;
        border-radius: 1rem; display: flex; justify-content: space-around;
        text-align: center; margin: 3rem 0; flex-wrap: wrap; gap: 1rem;
    }}
    .stats-bar h3, .stats-bar p {{ color: white !important; }} /* Forzar texto blanco en barra azul */

    /* IMAGENES */
    .hero-image {{
        background-image: url('{url_hero}');
        background-size: cover; background-position: center;
        height: 400px; border-radius: 20px;
        display: flex; align-items: center; justify-content: center;
        border: 4px solid white;
        box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1);
    }}
    .img-industry {{
        background-image: url('{url_ind}');
        background-size: cover; background-position: center;
        height: 300px; border-radius: 15px;
    }}
    .img-home {{
        background-image: url('{url_home}');
        background-size: cover; background-position: center;
        height: 300px; border-radius: 15px;
    }}

    .step-circle {{
        width: 4rem; height: 4rem; background: var(--primary); color: white !important;
        border-radius: 50%; display: flex; align-items: center; justify-content: center;
        font-size: 1.5rem; font-weight: bold; margin: 0 auto 1rem auto;
        border: 4px solid white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }}
    
    .section-divider {{ margin-top: 5rem; margin-bottom: 2rem; }}
    
    /* Títulos forzados a azul */
    h1, h2, h3, h4, h5, h6 {{
        color: var(--primary) !important;
    }}

</style>
""", unsafe_allow_html=True)

# ============================================
# 3. NAVBAR
# ============================================
st.markdown("""
<nav class="navbar">
    <a href="#inicio" class="nav-logo"> AInomaly</a>
    <div class="nav-links">
        <a href="#inicio" class="nav-link">Inicio</a>
        <a href="#diferencia" class="nav-link">Tecnología</a>
        <a href="#sectores" class="nav-link">Sectores</a>
        <a href="#demo" class="nav-link">Demo</a>
        <a href="#contacto" class="nav-link nav-cta">Solicitar Demo</a>
    </div>
</nav>
<br><br>
""", unsafe_allow_html=True)

# ============================================
# 4. CONTENIDO (SINGLE PAGE)
# ============================================

# --- HERO SECTION ---
st.markdown('<div id="inicio"></div>', unsafe_allow_html=True)
col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown("""
    <div style="background-color: #FEF9C3; color: #854D0E; padding: 5px 12px; border-radius: 20px; display: inline-block; font-size: 0.8rem; font-weight: 600; margin-bottom: 1rem;">
    Tecnología de Detección Avanzada
    </div>
    """, unsafe_allow_html=True)
    st.title("AInomaly")
    st.markdown("<h2 style='font-size: 2rem; margin-top: -10px;'>Detector Inteligente de Anomalías</h2>", unsafe_allow_html=True)
    st.markdown("""
    <p style="font-size: 1.25rem; font-style: italic; margin-top: 1rem;">"Donde otros ven video, nosotros vemos riesgos."</p>
    <p style="font-size: 1.1rem; line-height: 1.6; margin-bottom: 2rem;">
        Transforma una cámara estándar en un sensor inteligente. Utilizando visión por computadora y heurística geométrica, AInomaly detecta caídas en tiempo real.
    </p>
    """, unsafe_allow_html=True)
    
    c1, c2 = st.columns([1,2])
    with c1:
        st.link_button("Solicitar Demo ➜", "#contacto", type="primary")

with col2:
    st.markdown('<div class="hero-image"></div>', unsafe_allow_html=True)

# BARRA ESTADÍSTICAS
st.markdown("""
<div class="stats-bar">
    <div><h3 style="color:#FFD700 !important; margin:0;">MediaPipe</h3><p style="margin:0; color:#BFDBFE !important;">Visión por Computadora</p></div>
    <div><h3 style="color:#FFD700 !important; margin:0;">&lt; 1seg</h3><p style="margin:0; color:#BFDBFE !important;">Tiempo de Respuesta</p></div>
    <div><h3 style="color:#FFD700 !important; margin:0;">24/7</h3><p style="margin:0; color:#BFDBFE !important;">Monitoreo Continuo</p></div>
    <div><h3 style="color:#FFD700 !important; margin:0;">Local</h3><p style="margin:0; color:#BFDBFE !important;">Procesamiento Privado</p></div>
</div>
""", unsafe_allow_html=True)

# --- DIFERENCIADORES ---
st.markdown('<div id="diferencia" class="section-divider"></div>', unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>Por qué AInomaly es Diferente?</h2>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

col_diff1, col_diff2, col_diff3, col_diff4 = st.columns(4)
with col_diff1:
    st.markdown('<div class="custom-card"><div class="icon-box">⚡</div><h4>Tiempo Real</h4><p>Sin latencia. Procesamiento inmediato.</p></div>', unsafe_allow_html=True)
with col_diff2:
    st.markdown('<div class="custom-card"><div class="icon-box">🔒</div><h4>Privacidad</h4><p>Análisis 100% local, el video no sale.</p></div>', unsafe_allow_html=True)
with col_diff3:
    st.markdown('<div class="custom-card"><div class="icon-box">📐</div><h4>Geometría</h4><p>Matemática vectorial, sin cajas negras.</p></div>', unsafe_allow_html=True)
with col_diff4:
    st.markdown('<div class="custom-card"><div class="icon-box">📲</div><h4>Alertas</h4><p>Telegram bot integrado con foto.</p></div>', unsafe_allow_html=True)

# --- SECTORES ---
st.markdown('<div id="sectores" class="section-divider"></div>', unsafe_allow_html=True)
st.markdown("<h2>Soluciones para Cada Necesidad</h2><hr>", unsafe_allow_html=True)

# Sector 1
s1, s2 = st.columns([1, 1])
with s1:
    st.subheader("Industria Manufacturera")
    st.markdown("""
    Protección para trabajadores en plantas y almacenes.
    *  Reduce accidentes laborales
    *  Cumplimiento normativo
    *  Monitoreo masivo
    """)
with s2:
    st.markdown('<div class="img-industry"></div>', unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# Sector 2
s3, s4 = st.columns([1, 1])
with s3:
    st.markdown('<div class="img-home"></div>', unsafe_allow_html=True)
with s4:
    st.subheader("Cuidado en el Hogar")
    st.markdown("""
    Seguridad para adultos mayores que viven solos.
    *  Tranquilidad familiar
    *  Independencia sin vigilancia invasiva
    *  Evidencia solo ante incidentes
    """)

# --- ARQUITECTURA ---
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>Arquitectura del Sistema</h2><br>", unsafe_allow_html=True)

a1, a2, a3, a4 = st.columns(4)
steps = [
    ("1", "The Eye", "Visión", "Captura video y extrae ecoordenadas."),
    ("2", "The Brain", "Lógica", "Analiza vectores y ángulos de caída."),
    ("3", "The Messenger", "IoT", "Envía alertas push al móvil (Telegram)."),
    ("4", "The Face", "Interfaz", "Dashboard de monitoreo.")
]

for col, (num, title, subt, desc) in zip([a1, a2, a3, a4], steps):
    with col:
        st.markdown(f"""
        <div class="custom-card" style="text-align: center;">
            <div class="step-circle">{num}</div>
            <h4>{title}</h4>
            <p style="font-size: 0.9rem;"><b>{subt}</b><br>{desc}</p>
        </div>
        """, unsafe_allow_html=True)

# --- DEMO ---
st.markdown('<div id="demo" class="section-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="background-color: #f8fafc; padding: 2rem; border-radius: 1rem; border: 1px dashed #cbd5e1;">
<h2 style="text-align: center;"> Demo Interactiva</h5>
<p style="text-align: center;">Simula el comportamiento del sistema.</p>
<br>
""", unsafe_allow_html=True)

d1, d2 = st.columns([1, 2])
with d1:
    st.subheader("Panel de Control")
    escenario = st.selectbox("Escenario", ["Persona Caminando", "Caída Súbita", "Desmayo Lento"])
    if st.button("🚨 Ejecutar Simulación", use_container_width=True):
        if "Caída" in escenario or "Desmayo" in escenario:
            st.error(f"¡ALERTA DETECTADA! {escenario}")
            st.toast("Enviando alerta...", icon="📲")
        else:
            st.success("Estado Normal.")
with d2:
    st.video("video_demo.mp4")  
st.markdown("</div>", unsafe_allow_html=True)

# --- CONTACTO ---
st.markdown('<div id="contacto" class="section-divider"></div>', unsafe_allow_html=True)
st.header("Comienza a Proteger Hoy")

c1, c2 = st.columns(2)
with c1:
    st.markdown("""
    <div class="custom-card" style="background: #000080; color: white;">
        <h3 style="color: #FFD700 !important;">Contáctanos</h3>
        <p style="color:white;">¿Tienes cámaras instaladas? Podemos integrarnos.</p>
        <br>
        <ul style="list-style: none; padding: 0;">
            <li style="margin-bottom: 10px; color:white;">📧 contacto@ainomaly.com</li>
            <li style="margin-bottom: 10px; color:white;">📞 +1 (800) 123-4567</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
with c2:
    with st.form("contact_form"):
        col_form1, col_form2 = st.columns(2)
        with col_form1: st.text_input("Nombre")
        with col_form2: st.text_input("Empresa")
        st.text_input("Email")
        st.form_submit_button("Enviar Solicitud", use_container_width=True)

# FOOTER
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="background: #000080; color: white; padding: 4rem 2rem; text-align: center;">
    <h3 style="color: white !important;">AInomaly</h3>
    <p style="color: #BFDBFE;">Inteligencia Artificial que cuida vidas.</p>
    <p style="font-size: 0.8rem; opacity: 0.6; color: #BFDBFE;">© 2025 AInomaly Technologies.</p>
</div>
""", unsafe_allow_html=True)