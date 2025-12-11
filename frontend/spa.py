import streamlit as st
import base64
import os

# ============================================
# 1. CONFIGURACIÓN DE PÁGINA
# ============================================
st.set_page_config(
    page_title="Alnomaly - Guardián Digital",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# 📍 CONFIGURACIÓN DE IMÁGENES (EDITA AQUÍ)
# ============================================
# Pon aquí el nombre exacto de tus archivos locales.
# Si no encuentra la imagen, usará una de internet por defecto para que no falle.

def get_base64_image(image_path):
    """Convierte imagen local a string base64 para CSS"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

# --- RUTAS DE TUS IMÁGENES ---
# Asegúrate de que estas imágenes estén en la misma carpeta o pon la ruta completa
ruta_hero_bg = "hero_obrero.jpg"       # <--- CAMBIA ESTO por tu foto del obrero
ruta_industria = "industria.jpg"       # <--- CAMBIA ESTO por tu foto de fábrica
ruta_hogar = "abuelo.jpg"              # <--- CAMBIA ESTO por tu foto del anciano

# --- PROCESAMIENTO (NO TOCAR) ---
img_hero_b64 = get_base64_image(ruta_hero_bg)
img_ind_b64 = get_base64_image(ruta_industria)
img_home_b64 = get_base64_image(ruta_hogar)

# Fallbacks (Si no encuentra tus fotos, usa estas de internet)
url_hero = f"data:image/jpeg;base64,{img_hero_b64}" if img_hero_b64 else "https://images.unsplash.com/photo-1541888946425-d81bb19240f5?q=80&w=1000&auto=format&fit=crop"
url_ind = f"data:image/jpeg;base64,{img_ind_b64}" if img_ind_b64 else "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&w=800"
url_home = f"data:image/jpeg;base64,{img_home_b64}" if img_home_b64 else "https://images.unsplash.com/photo-1576765608535-5f04d1e3f289?auto=format&fit=crop&w=800"


# ============================================
# 2. ESTILOS CSS
# ============================================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    :root {{
        --primary: #000080;
        --accent: #FFD700;
        --text-dark: #1F2937;
    }}

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
        scroll-behavior: smooth;
    }}
    
    #MainMenu, footer, header {{visibility: hidden;}}
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
    .nav-link {{ color: #4B5563; text-decoration: none; font-weight: 600; transition: color 0.3s; }}
    .nav-link:hover {{ color: var(--primary); }}
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

    /* IMAGENES DE FONDO DINÁMICAS (Aquí usamos las variables Python) */
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
        width: 4rem; height: 4rem; background: var(--primary); color: white;
        border-radius: 50%; display: flex; align-items: center; justify-content: center;
        font-size: 1.5rem; font-weight: bold; margin: 0 auto 1rem auto;
        border: 4px solid white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }}
    
    .section-divider {{ margin-top: 5rem; margin-bottom: 2rem; }}

</style>
""", unsafe_allow_html=True)

# ============================================
# 3. NAVBAR
# ============================================
st.markdown("""
<nav class="navbar">
    <a href="#inicio" class="nav-logo">🛡️ Alnomaly</a>
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
        🛡️ Tecnología de Detección Avanzada
    </div>
    """, unsafe_allow_html=True)
    st.title("Alnomaly")
    st.markdown("<h2 style='font-size: 2rem; margin-top: -10px; color:#000080;'>Detector Inteligente de Anomalías</h2>", unsafe_allow_html=True)
    st.markdown("""
    <p style="font-size: 1.25rem; font-style: italic; color: #4B5563; margin-top: 1rem;">"Donde otros ven video, nosotros vemos riesgos."</p>
    <p style="font-size: 1.1rem; line-height: 1.6; color: #374151; margin-bottom: 2rem;">
        Transforma una cámara estándar en un sensor inteligente. Utilizando visión por computadora y heurística geométrica, Alnomaly detecta caídas en tiempo real.
    </p>
    """, unsafe_allow_html=True)
    
    c1, c2 = st.columns([1,2])
    with c1:
        st.link_button("Solicitar Demo ➜", "#contacto", type="primary")

with col2:
    # Usamos la clase .hero-image que tiene inyectado el B64
    st.markdown('<div class="hero-image"></div>', unsafe_allow_html=True)

# BARRA ESTADÍSTICAS
st.markdown("""
<div class="stats-bar">
    <div><h3 style="color:#FFD700 !important; margin:0;">MediaPipe</h3><p style="margin:0; color:#BFDBFE;">Visión por Computadora</p></div>
    <div><h3 style="color:#FFD700 !important; margin:0;">&lt; 1seg</h3><p style="margin:0; color:#BFDBFE;">Tiempo de Respuesta</p></div>
    <div><h3 style="color:#FFD700 !important; margin:0;">24/7</h3><p style="margin:0; color:#BFDBFE;">Monitoreo Continuo</p></div>
    <div><h3 style="color:#FFD700 !important; margin:0;">Local</h3><p style="margin:0; color:#BFDBFE;">Procesamiento Privado</p></div>
</div>
""", unsafe_allow_html=True)

# --- DIFERENCIADORES ---
st.markdown('<div id="diferencia" class="section-divider"></div>', unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color:#000080;'>Por qué Alnomaly es Diferente</h2>", unsafe_allow_html=True)
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
st.markdown("<h2 style='color:#000080;'>Soluciones para Cada Necesidad</h2><hr>", unsafe_allow_html=True)

# Sector 1
s1, s2 = st.columns([1, 1])
with s1:
    st.markdown('<div style="background:#FEF9C3; color:#854D0E; padding:4px 10px; border-radius:4px; display:inline-block; font-weight:bold; font-size:0.8rem; margin-bottom:10px;">SECTOR</div>', unsafe_allow_html=True)
    st.subheader("Industria Manufacturera")
    st.markdown("""
    Protección para trabajadores en plantas y almacenes.
    * ✅ Reduce accidentes laborales
    * ✅ Cumplimiento normativo
    * ✅ Monitoreo masivo
    """)
with s2:
    st.markdown('<div class="img-industry"></div>', unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# Sector 2
s3, s4 = st.columns([1, 1])
with s3:
    st.markdown('<div class="img-home"></div>', unsafe_allow_html=True)
with s4:
    st.markdown('<div style="background:#FEF9C3; color:#854D0E; padding:4px 10px; border-radius:4px; display:inline-block; font-weight:bold; font-size:0.8rem; margin-bottom:10px;">SECTOR</div>', unsafe_allow_html=True)
    st.subheader("Cuidado en el Hogar")
    st.markdown("""
    Seguridad para adultos mayores que viven solos.
    * ✅ Tranquilidad familiar
    * ✅ Independencia sin vigilancia invasiva
    * ✅ Evidencia solo ante incidentes
    """)

# --- ARQUITECTURA ---
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color:#000080;'>Arquitectura del Sistema</h2><br>", unsafe_allow_html=True)

a1, a2, a3, a4 = st.columns(4)
steps = [
    ("1", "The Eye", "Visión", "Captura video y extrae esqueletos (MediaPipe)."),
    ("2", "The Brain", "Lógica", "Analiza vectores y ángulos de caída."),
    ("3", "The Messenger", "IoT", "Envía alertas push al móvil (Telegram)."),
    ("4", "The Face", "Interfaz", "Dashboard de monitoreo (Streamlit).")
]

for col, (num, title, subt, desc) in zip([a1, a2, a3, a4], steps):
    with col:
        st.markdown(f"""
        <div class="custom-card" style="text-align: center;">
            <div class="step-circle">{num}</div>
            <h4 style="color:#000080;">{title}</h4>
            <p style="font-size: 0.9rem;"><b>{subt}</b><br>{desc}</p>
        </div>
        """, unsafe_allow_html=True)

# --- DEMO ---
st.markdown('<div id="demo" class="section-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="background-color: #f8fafc; padding: 2rem; border-radius: 1rem; border: 1px dashed #cbd5e1;">
<h2 style="text-align: center; color:#000080;">📱 Demo Interactiva</h2>
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
    st.markdown("""
    <div style="background: black; height: 350px; border-radius: 10px; display: flex; align-items: center; justify-content: center; position: relative; overflow: hidden;">
        <div style="position: absolute; top: 15px; left: 15px; background: red; color: white; padding: 5px 10px; border-radius: 4px; font-weight: bold; font-size: 0.8rem; animation: pulse 2s infinite;">🔴 EN VIVO</div>
        <p style="color: white; text-align: center;">📹 Feed de Video<br><span style="color:#00ff00; font-family:monospace;">Analizando...</span></p>
    </div>
    """, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- CONTACTO ---
st.markdown('<div id="contacto" class="section-divider"></div>', unsafe_allow_html=True)
st.header("Comienza a Proteger Hoy")

c1, c2 = st.columns(2)
with c1:
    st.markdown("""
    <div class="custom-card" style="background: #000080; color: white;">
        <h3 style="color: #FFD700 !important;">Contáctanos</h3>
        <p>¿Tienes cámaras instaladas? Podemos integrarnos.</p>
        <br>
        <ul style="list-style: none; padding: 0;">
            <li style="margin-bottom: 10px;">📧 contacto@alnomaly.com</li>
            <li style="margin-bottom: 10px;">📞 +1 (800) 123-4567</li>
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
    <h3 style="color: white !important;">Alnomaly</h3>
    <p style="color: #BFDBFE;">Inteligencia Artificial que cuida vidas.</p>
    <p style="font-size: 0.8rem; opacity: 0.6;">© 2025 Alnomaly Technologies.</p>
</div>
""", unsafe_allow_html=True)