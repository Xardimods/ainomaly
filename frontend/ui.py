import streamlit as st
from PIL import Image
import base64

# ============================================
# 1. CONFIGURACIÓN DE PÁGINA
# ============================================
st.set_page_config(
    page_title="Alnomaly - Detección Inteligente",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# 2. ESTILOS CSS PERSONALIZADOS (El Diseño Visual)
# ============================================
# Aquí inyectamos el CSS para copiar el estilo de la landing HTML (Tailwind-like)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    /* Variables de color basadas en tu diseño */
    :root {
        --primary: #000080;   /* Azul Marino */
        --accent: #FFD700;    /* Amarillo */
        --bg-light: #F3F4F6;
        --text-dark: #1F2937;
    }

    /* Fuente general */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: var(--text-dark);
    }

    /* Títulos */
    h1, h2, h3 {
        color: var(--primary) !important;
        font-weight: 700 !important;
    }

    /* Fondo de la app principal */
    .stApp {
        background-color: white;
    }

    /* === COMPONENTES PERSONALIZADOS === */

    /* Tarjeta estilo Landing Page */
    .custom-card {
        background-color: white;
        padding: 2rem;
        border-radius: 1rem;
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: transform 0.2s;
        height: 100%;
    }
    .custom-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        border-color: #BFDBFE;
    }

    /* Iconos en tarjetas */
    .icon-box {
        width: 3rem;
        height: 3rem;
        background-color: #FEF9C3; /* Amarillo claro */
        color: var(--primary);
        border-radius: 0.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }

    /* Barra de Estadísticas Azul */
    .stats-bar {
        background-color: var(--primary);
        color: white;
        padding: 2rem;
        border-radius: 1rem;
        display: flex;
        justify-content: space-around;
        text-align: center;
        margin: 2rem 0;
    }
    .stat-item h3 { color: var(--accent) !important; margin: 0; font-size: 1.5rem; }
    .stat-item p { color: #BFDBFE; margin: 0; font-size: 0.9rem; }

    /* Botones de Streamlit personalizados */
    div.stButton > button {
        background-color: var(--primary);
        color: white;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        border: none;
        font-weight: 600;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: #000060;
        color: var(--accent);
    }

    /* Badge pequeña */
    .badge {
        background-color: #FEF9C3;
        color: #854D0E;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 1rem;
        border: 1px solid #FEF08A;
    }

    /* Círculos de pasos (Arquitectura) */
    .step-circle {
        width: 4rem;
        height: 4rem;
        background-color: var(--primary);
        color: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        font-weight: bold;
        margin: 0 auto 1rem auto;
        border: 4px solid white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

</style>
""", unsafe_allow_html=True)

# ============================================
# 3. BARRA LATERAL (NAVEGACIÓN)
# ============================================
with st.sidebar:
    # Si tienes un logo, descomenta esto:
    # st.image("logo.png", width=150)
    
    st.markdown("<h2 style='text-align: center;'>🛡️ Alnomaly</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Menú de navegación
    page = st.radio(
        "Navegación",
        ["🏠 Inicio", "💡 Soluciones (Sectores)", "⚙️ Arquitectura", "✨ Características", "📱 Demo Interactiva", "📞 Contacto"]
    )
    
    st.markdown("---")
    st.info("Estado del Sistema: 🟢 Activo")
    st.caption("v2.4.0 - Build 2025")

# ============================================
# 4. CONTENIDO DE LAS PÁGINAS
# ============================================

# --- PÁGINA: INICIO (HERO SECTION) ---
if page == "🏠 Inicio":
    
    # Hero Section
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.markdown("""
        <div class="badge">
            <span>🛡️</span> Tecnología de Detección Avanzada con IA
        </div>
        """, unsafe_allow_html=True)
        
        st.title("Alnomaly")
        st.markdown("<h2 style='font-size: 1.8rem; margin-top: -15px; opacity: 0.9;'>Detector Inteligente de Anomalías y Caídas</h2>", unsafe_allow_html=True)
        
        st.markdown("""
        <p style="font-size: 1.2rem; font-style: italic; color: #4B5563; margin-bottom: 1.5rem;">
            "Donde otros ven video, nosotros vemos riesgos."
        </p>
        <p style="font-size: 1.1rem; line-height: 1.6; color: #374151; margin-bottom: 2rem;">
            Transforma una cámara estándar en un sensor inteligente. Utilizando visión por computadora y heurística geométrica, 
            Alnomaly detecta caídas y comportamientos anómalos en tiempo real.
        </p>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Solicitar Demo ➜"):
                st.toast("Redirigiendo a solicitud de demo...")
        with c2:
            st.button("Ver Características", type="secondary")

    with col2:
        # Placeholder para imagen (puedes reemplazar con st.image("tu_imagen.jpg"))
        st.markdown("""
        <div style="background-color: #EEE; height: 400px; border-radius: 20px; display: flex; align-items: center; justify-content: center; border: 4px solid white; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);">
            <p style="color: #999;">[Imagen Hero: Obrero Cayendo]</p>
        </div>
        """, unsafe_allow_html=True)

    # Barra Azul de Estadísticas
    st.markdown("""
    <div class="stats-bar">
        <div class="stat-item">
            <h3>MediaPipe</h3>
            <p>Visión por Computadora</p>
        </div>
        <div class="stat-item">
            <h3>< 1seg</h3>
            <p>Tiempo de Respuesta</p>
        </div>
        <div class="stat-item">
            <h3>24/7</h3>
            <p>Monitoreo Continuo</p>
        </div>
        <div class="stat-item">
            <h3>Local</h3>
            <p>Procesamiento Privado</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Diferenciadores (Grid 2x2)
    st.subheader("Por qué Alnomaly es diferente")
    st.markdown("<br>", unsafe_allow_html=True)
    
    d1, d2 = st.columns(2)
    with d1:
        st.markdown("""
        <div class="custom-card">
            <div class="icon-box">⚡</div>
            <h3>Detección en Tiempo Real</h3>
            <p>Procesamiento inmediato de frames de video sin latencia. Respuesta instantánea.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="custom-card">
            <div class="icon-box">📐</div>
            <h3>Lógica Geométrica</h3>
            <p>Alta precisión basada en vectores y ángulos, sin necesidad de redes pesadas.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with d2:
        st.markdown("""
        <div class="custom-card">
            <div class="icon-box">🔒</div>
            <h3>Privacidad Total</h3>
            <p>El análisis ocurre localmente. Solo se transmiten alertas, nunca video continuo.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="custom-card">
            <div class="icon-box">📱</div>
            <h3>Alertas Remotas</h3>
            <p>Conexión directa al móvil del cuidador vía Telegram con evidencia fotográfica.</p>
        </div>
        """, unsafe_allow_html=True)

# --- PÁGINA: SOLUCIONES (SECTORES) ---
elif page == "💡 Soluciones (Sectores)":
    st.header("Soluciones para Cada Necesidad")
    st.markdown("Adaptamos nuestro sistema a diferentes ambientes.")
    st.divider()

    # Sector Industria
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style="background-color: #FEF9C3; color: #854D0E; padding: 5px 10px; border-radius: 5px; display: inline-block; font-weight: bold; font-size: 0.8rem; margin-bottom: 10px;">SECTOR</div>
        """, unsafe_allow_html=True)
        st.subheader("Industria Manufacturera")
        st.markdown("""
        Protección para trabajadores en plantas de producción, almacenes y líneas de ensamblaje. 
        Una cámara cubre amplias áreas sin necesidad de sensores individuales.
        
        * ✅ Reduce accidentes laborales
        * ✅ Cumplimiento normativo
        * ✅ Monitoreo de múltiples trabajadores
        """)
    with col2:
        st.markdown("""
        <div style="background-color: #DDD; height: 250px; border-radius: 15px; display: flex; align-items: center; justify-content: center;">
            <p>[Imagen Industria]</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Sector Hogar
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("""
        <div style="background-color: #DDD; height: 250px; border-radius: 15px; display: flex; align-items: center; justify-content: center;">
            <p>[Imagen Cuidado Hogar]</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div style="background-color: #FEF9C3; color: #854D0E; padding: 5px 10px; border-radius: 5px; display: inline-block; font-weight: bold; font-size: 0.8rem; margin-bottom: 10px;">SECTOR</div>
        """, unsafe_allow_html=True)
        st.subheader("Cuidado en el Hogar")
        st.markdown("""
        Seguridad para adultos mayores y personas con movilidad reducida que viven solas. 
        Alertas instantáneas a familiares sin invadir la privacidad.
        
        * ✅ Tranquilidad para familias
        * ✅ Independencia sin vigilancia invasiva
        * ✅ Evidencia fotográfica del incidente
        """)

# --- PÁGINA: ARQUITECTURA ---
elif page == "⚙️ Arquitectura":
    st.header("Arquitectura del Sistema")
    st.markdown("Cuatro módulos principales operando en simultáneo.")
    st.markdown("<br><br>", unsafe_allow_html=True)

    # Layout de 4 columnas para los pasos
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown("""
        <div class="custom-card" style="text-align: center;">
            <div class="step-circle">1</div>
            <h4 style="color:#000080;">The Eye</h4>
            <p style="font-size: 0.9rem;"><b>Visión</b><br>Captura video y extrae el esqueleto humano mediante MediaPipe.</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="custom-card" style="text-align: center;">
            <div class="step-circle">2</div>
            <h4 style="color:#000080;">The Brain</h4>
            <p style="font-size: 0.9rem;"><b>Lógica</b><br>Analiza vectores y ángulos geométricos para identificar caídas.</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="custom-card" style="text-align: center;">
            <div class="step-circle">3</div>
            <h4 style="color:#000080;">The Messenger</h4>
            <p style="font-size: 0.9rem;"><b>IoT</b><br>Envía notificaciones push con evidencia vía Telegram.</p>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class="custom-card" style="text-align: center;">
            <div class="step-circle">4</div>
            <h4 style="color:#000080;">The Face</h4>
            <p style="font-size: 0.9rem;"><b>Interfaz</b><br>Dashboard interactivo en Streamlit (¡Esta App!).</p>
        </div>
        """, unsafe_allow_html=True)

# --- PÁGINA: CARACTERÍSTICAS (Grid) ---
elif page == "✨ Características":
    st.header("Características que Salvan Vidas")
    st.markdown("<br>", unsafe_allow_html=True)

    # Primera Fila
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="custom-card">
            <div class="icon-box">📷</div>
            <h4>Cámara Estándar</h4>
            <p style="font-size:0.9rem;">No requiere sensores especiales. Convierte cualquier cámara web o IP.</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="custom-card">
            <div class="icon-box">👁️</div>
            <h4>Visión Computarizada</h4>
            <p style="font-size:0.9rem;">Análisis de esqueleto completo para entender la postura humana.</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="custom-card">
            <div class="icon-box">📐</div>
            <h4>Heurística</h4>
            <p style="font-size:0.9rem;">Matemática vectorial para diferenciar una caída de agacharse.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Segunda Fila
    c4, c5, c6 = st.columns(3)
    with c4:
        st.markdown("""
        <div class="custom-card">
            <div class="icon-box">🔒</div>
            <h4>Privacidad</h4>
            <p style="font-size:0.9rem;">Procesamiento local. Tus imágenes no van a la nube de terceros.</p>
        </div>
        """, unsafe_allow_html=True)
    with c5:
        st.markdown("""
        <div class="custom-card">
            <div class="icon-box">📲</div>
            <h4>Telegram Bot</h4>
            <p style="font-size:0.9rem;">Alertas instantáneas en tu bolsillo con foto del evento.</p>
        </div>
        """, unsafe_allow_html=True)
    with c6:
        st.markdown("""
        <div class="custom-card">
            <div class="icon-box">⏱️</div>
            <h4>Tiempo Real</h4>
            <p style="font-size:0.9rem;">Sin latencia perceptible. Detección en milisegundos.</p>
        </div>
        """, unsafe_allow_html=True)

# --- PÁGINA: DEMO INTERACTIVA (Funcionalidad Python original) ---
elif page == "📱 Demo Interactiva":
    st.title("📱 Prueba de Concepto")
    st.markdown("Interactúa con el sistema como si fueras un operador.")
    
    col_demo1, col_demo2 = st.columns([1, 2])
    
    with col_demo1:
        st.markdown("### Panel de Control")
        st.markdown("""<div class="custom-card">""", unsafe_allow_html=True)
        
        escenario = st.selectbox(
            "Seleccionar Escenario Simulado:",
            ["Caída en pasillo", "Desmayo repentino", "Movimiento inusual", "Normal"]
        )
        
        sensibilidad = st.slider("Sensibilidad de Detección", 0, 100, 75)
        
        notif_on = st.toggle("Activar Notificaciones", value=True)
        
        if st.button("🚨 EJECUTAR SIMULACIÓN"):
            if escenario == "Normal":
                 st.success("✅ Sistema estable. Sin anomalías.")
            else:
                st.error(f"⚠️ ¡ALERTA! {escenario} detectado.")
                if notif_on:
                    st.toast(f"Mensaje enviado a Supervisor: {escenario}", icon="📲")
        
        st.markdown("</div>", unsafe_allow_html=True)

    with col_demo2:
        st.markdown("### Visualización en Vivo")
        # Simulación de ventana de video
        st.markdown("""
        <div style="background-color: black; width: 100%; height: 400px; border-radius: 10px; position: relative; display: flex; align-items: center; justify-content: center; overflow: hidden;">
            <p style="color: white;">[Video Feed Stream]</p>
            <div style="position: absolute; top: 15px; left: 15px; background: red; color: white; padding: 5px 10px; border-radius: 4px; font-weight: bold; font-size: 0.8rem; animation: pulse 2s infinite;">🔴 EN VIVO</div>
            <div style="position: absolute; bottom: 15px; left: 15px; color: #00ff00; font-family: monospace;">FPS: 30 | LATENCY: 12ms</div>
            <div style="position: absolute; width: 100%; height: 100%; background: linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px) 0 0 / 50px 50px, linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px) 0 0 / 50px 50px;"></div>
        </div>
        """, unsafe_allow_html=True)

# --- PÁGINA: CONTACTO ---
elif page == "📞 Contacto":
    st.header("Comienza a Proteger lo que Más Importa")
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("""
        <div class="custom-card">
            <h3>Contáctanos</h3>
            <p>Agenda una demostración personalizada.</p>
            <br>
            <p>📧 <b>Email:</b> contacto@alnomaly.com</p>
            <p>📞 <b>Tel:</b> +1 (800) 123-4567</p>
            <p>🏢 <b>Oficinas:</b> Ciudad Tecnológica, Edificio AI</p>
        </div>
        """, unsafe_allow_html=True)
    
    with c2:
        with st.form("contact_form"):
            st.markdown("### Envíanos un mensaje")
            nombre = st.text_input("Nombre")
            email = st.text_input("Correo Electrónico")
            mensaje = st.text_area("Mensaje")
            
            submit = st.form_submit_button("Enviar Mensaje")
            if submit:
                st.success("¡Gracias! Tu mensaje ha sido enviado.")

# ============================================
# 5. FOOTER
# ============================================
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="background-color: #000080; color: white; padding: 3rem; text-align: center; border-radius: 1rem 1rem 0 0;">
    <h3>Alnomaly</h3>
    <p style="color: #BFDBFE;">Tu guardián digital inteligente</p>
    <br>
    <p style="font-size: 0.8rem; opacity: 0.7;">© 2025 Alnomaly Technologies. Todos los derechos reservados.</p>
</div>
""", unsafe_allow_html=True)