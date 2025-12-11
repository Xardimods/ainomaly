# AInomaly_app.py
# Archivo principal de la aplicación Streamlit para AInomaly

import streamlit as st
import base64
from PIL import Image
import io
from pathlib import Path

# Configuración de la página
st.set_page_config(
    page_title="AInomaly - Guardián Digital",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# FUNCIONES AUXILIARES
# ============================================

def add_bg_from_local(image_file):
    """Función para agregar fondo de imagen"""
    with open(image_file, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{encoded_string});
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def card_component(title, content, icon=None):
    """Componente de tarjeta para presentar información"""
    icon_html = f"<div style='font-size: 2.5rem; margin-bottom: 10px;'>{icon}</div>" if icon else ""
    
    card_html = f"""
    <div style='
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #4A6FA5;
        min-height: 200px;
        transition: transform 0.3s;
    '>
        {icon_html}
        <h3 style='color: #2C3E50; margin-top: 0;'>{title}</h3>
        <p style='color: #FFFF; line-height: 1.6;'>{content}</p>
    </div>
    """
    return card_html

# ============================================
# ENCABEZADO Y NAVEGACIÓN
# ============================================

# Barra lateral para navegación
with st.sidebar:
    current_dir = Path(__file__).resolve().parent
    logo_path = current_dir / "Logo_AInomaly.png"

    st.image(str(logo_path), width=80)
    st.title("🛡️ AInomaly")
    st.markdown("---")
    
    # Navegación
    page = st.radio(
        "Navegación",
        ["🏠 Inicio", "🔍 El Problema", "💡 La Solución", "✨ Beneficios", "📱 Cómo Funciona", "📞 Contacto"]
    )
    
    st.markdown("---")
    st.markdown("### Demostración")
    if st.button("🎬 Ver Demo en Vivo"):
        st.info("Funcionalidad de demo disponible en versión completa ;)")
    
    st.markdown("---")
    st.markdown("""
    <div style='background-color: #fffff; padding: 15px; border-radius: 10px;'>
    <small>🛡️ Transformando cámaras comunes en sistemas de seguridad inteligentes</small>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# PÁGINA PRINCIPAL
# ============================================

if page == "🏠 Inicio":
    
    # Header principal
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(
            """
            <div style='padding: 20px 0;'>
            <h1 style='color: #ffde59; font-size: 3.5rem; margin-bottom: 10px;'>
            🛡️ AInomaly
            </h1>
            <h2 style='color: #ffde59; font-size: 1.8rem; margin-top: 0;'>
            Tu Guardián Digital Inteligente
            </h2>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown(
            """
            <div style='background: linear-gradient(135deg, #4A6FA5, #2C3E50); 
                        padding: 30px; 
                        border-radius: 15px;
                        color: white;
                        margin: 20px 0;'>
            <h3 style='color: white;'>🚨 Transformamos cualquier cámara común en un sistema inteligente</h3>
            <p style='font-size: 1.2rem;'>
            Detectamos caídas y situaciones peligrosas en tiempo real, sin necesidad de comprar equipos nuevos.
            </p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        # Espacio para imagen principal
        st.markdown(
            """
            <div style='background-color: #f8f9fa; 
                        padding: 20px; 
                        border-radius: 15px;
                        text-align: center;
                        height: 300px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        border: 2px dashed #4A6FA5;'>
            <p style='color: #4A6FA5;'>📷 Espacio para imagen de AInomaly en acción</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        # Nota para el usuario: Aquí puedes agregar tu imagen con:
        # st.image("ruta_de_tu_imagen.jpg", use_column_width=True)
    

    # Mensaje emocional
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col2:
        st.markdown(
            """
            <div style='text-align: center; padding: 25px; background-color: #FFFFF; color: white; border-radius: 30px;'>
            <h3 style='color: white;'>
            <p style='font-size: 1.1rem;'>
            No vendemos un software. Vendemos <strong>tranquilidad</strong>: 
            Saber que si algo le pasa a alguien bajo la responsabilidad de la empresa, 
            no será ignorado ni descubierto demasiado tarde.
            </p>
            </div>
            """,
            unsafe_allow_html=True
        )

# ============================================
# PÁGINA: EL PROBLEMA
# ============================================

elif page == "🔍 El Problema":
    
    st.title("🔍 El Problema que Resolvemos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(card_component(
            "👵 Personas Vulnerables",
            "Empresas que manejan adultos mayores, pacientes, trabajadores en riesgo o necesitan vigilancia constante enfrentan desafíos de seguridad diarios.",
            "👵"
        ), unsafe_allow_html=True)
        
        st.markdown(card_component(
            "⏰ Detección Tardía",
            "Normalmente las caídas y situaciones peligrosas se detectan tarde, cuando ya pasó lo peor. Cada minuto cuenta en una emergencia.",
            "⏰"
        ), unsafe_allow_html=True)
    
    with col2:
        # Espacio para imagen ilustrativa del problema
        st.markdown(
            """
            <div style='background-color: #f8f9fa; 
                        padding: 20px; 
                        border-radius: 15px;
                        text-align: center;
                        height: 300px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        margin-top: 80px;
                        border: 2px dashed #ffde59;'>
            <p style='color: #e74c3c;'>🖼️ Espacio para imagen ilustrando el problema</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Estadísticas (puedes personalizar)
    st.markdown("---")
    st.markdown("### El Impacto Real")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            """
            <div style='text-align: center; padding: 20px; background-color: #FFFFF; border-radius: 10px;'>
            <h1 style='color: #e74c3c;'>30%</h1>
            <p>De adultos mayores sufren caídas anuales</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            """
            <div style='text-align: center; padding: 20px; background-color: #FFFFF; border-radius: 10px;'>
            <h1 style='color: #e74c3c;'>65%</h1>
            <p>De accidentes laborales son por caídas</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            """
            <div style='text-align: center; padding: 20px; background-color: #FFFFF; border-radius: 10px;'>
            <h1 style='color: #e74c3c;'>+30 min</h1>
            <p>Tiempo promedio de respuesta actual</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col4:
        st.markdown(
            """
            <div style='text-align: center; padding: 20px; background-color: #FFFFF; border-radius: 10px;'>
            <h1 style='color: #e74c3c;'>90%</h1>
            <p>Reducción posible con detección inmediata</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# ============================================
# PÁGINA: LA SOLUCIÓN
# ============================================

elif page == "💡 La Solución":
    
    st.title("💡 ¿Qué hace AInomaly?")
    
    st.markdown(
        """
        <div style='background: linear-gradient(135deg, #4A6FA5, #2C3E50); 
                    padding: 30px; 
                    border-radius: 15px;
                    color: white;
                    margin: 20px 0;'>
        <h2 style='color: white;'>👁️ Observa silenciosamente y actúa inmediatamente</h2>
        <p style='font-size: 1.2rem;'>
        AInomaly no se queda solo mirando: cuando detecta una caída o situación peligrosa, 
        envía una alerta inmediata al celular del encargado para que puedan actuar rápido.
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Características principales
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(card_component(
            "🚨 Alertas Inmediatas",
            "Notificaciones instantáneas al teléfono del supervisor cuando detecta una caída o situación anormal.",
            "🚨"
        ), unsafe_allow_html=True)
        
        st.markdown(card_component(
            "🤖 IA Avanzada",
            "Algoritmos de inteligencia artificial entrenados para reconocer patrones de caídas y situaciones de riesgo.",
            "🤖"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(card_component(
            "📱 Interfaz Sencilla",
            "Panel de control intuitivo que cualquier persona puede usar sin necesidad de entrenamiento especializado.",
            "📱"
        ), unsafe_allow_html=True)
        
        st.markdown(card_component(
            "⚡ Tiempo Real",
            "Análisis continuo de video 24/7 sin retrasos. Cada segundo cuenta en una emergencia.",
            "⚡"
        ), unsafe_allow_html=True)
    
    # Diagrama de funcionamiento (simulado)
    st.markdown("---")
    st.markdown("### 🔄 Flujo de Funcionamiento")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            """
            <div style='text-align: center;'>
            <div style='background-color: #4A6FA5; color: white; width: 60px; height: 60px; 
                        border-radius: 50%; display: flex; align-items: center; 
                        justify-content: center; margin: 0 auto; font-size: 1.5rem;'>
            1
            </div>
            <h4>Cámara Existente</h4>
            <p>Usa tu equipo actual</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            """
            <div style='text-align: center;'>
            <div style='background-color: #4A6FA5; color: white; width: 60px; height: 60px; 
                        border-radius: 50%; display: flex; align-items: center; 
                        justify-content: center; margin: 0 auto; font-size: 1.5rem;'>
            2
            </div>
            <h4>Análisis IA</h4>
            <p>Detección en tiempo real</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            """
            <div style='text-align: center;'>
            <div style='background-color: #4A6FA5; color: white; width: 60px; height: 60px; 
                        border-radius: 50%; display: flex; align-items: center; 
                        justify-content: center; margin: 0 auto; font-size: 1.5rem;'>
            3
            </div>
            <h4>Alerta Instantánea</h4>
            <p>Notificación al supervisor</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col4:
        st.markdown(
            """
            <div style='text-align: center;'>
            <div style='background-color: #4A6FA5; color: white; width: 60px; height: 60px; 
                        border-radius: 50%; display= flex; align-items: center; 
                        justify-content: center; margin: 0 auto; font-size: 1.5rem;'>
            4
            </div>
            <h4>Respuesta Rápida</h4>
            <p>Acción inmediata</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Flechas entre pasos (simuladas con HTML)
    st.markdown(
        """
        <div style='display: flex; justify-content: space-between; padding: 0 40px; margin-top: -20px;'>
        <div style='font-size: 1.5rem;'>→</div>
        <div style='font-size: 1.5rem;'>→</div>
        <div style='font-size: 1.5rem;'>→</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================
# PÁGINA: BENEFICIOS
# ============================================

elif page == "✨ Beneficios":
    
    st.title("✨ Beneficios que tu Empresa Sí Entiende")
    
    # Beneficios en tarjetas
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(card_component(
            "💰 Reduce Costos",
            "Menos accidentes graves → baja costos médicos y reclamaciones legales. Inversión que se recupera rápidamente.",
            "💰"
        ), unsafe_allow_html=True)
        
        st.markdown(card_component(
            "⚡ Respuesta Inmediata",
            "El personal actúa más rápido y salva situaciones antes de que empeoren. Cada segundo cuenta.",
            "⚡"
        ), unsafe_allow_html=True)
        
        st.markdown(card_component(
            "🔧 Sin Hardware Nuevo",
            "Usa las cámaras que ya tienes. No necesitas comprar equipos especializados ni llenar el lugar de sensores.",
            "🔧"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(card_component(
            "👨‍💻 Fácil de Usar",
            "Panel sencillo e intuitivo, sin entrenamientos complicados. Tus empleados lo dominarán en minutos.",
            "👨‍💻"
        ), unsafe_allow_html=True)
        
        st.markdown(card_component(
            "🔒 Privado y Seguro",
            "Todo el análisis se realiza localmente; solo se envían alertas. Tus videos nunca salen de tus instalaciones.",
            "🔒"
        ), unsafe_allow_html=True)
        
        st.markdown(card_component(
            "🌙 Operación 24/7",
            "Nunca se cansa, nunca se distrae. Monitoreo constante día y noche, fines de semana y festivos.",
            "🌙"
        ), unsafe_allow_html=True)
    
    # Casos de uso
    st.markdown("---")
    st.markdown("### 🏥 Casos de Uso Ideales")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            """
            <div style='background-color: #FFFFF; padding: 20px; border-radius: 10px; height: 150px;'>
            <h4 style='color: #ffde59;'>🏥 Hospitales y Clínicas</h4>
            <p>Monitoreo de pacientes en habitaciones y áreas comunes</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            """
            <div style='background-color: #FFFFF; padding: 20px; border-radius: 10px; height: 150px;'>
            <h4 style='color: #ffde59;'>👵 Residencias de Ancianos</h4>
            <p>Protección de adultos mayores en sus actividades diarias</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            """
            <div style='background-color: #FFFFf; padding: 20px; border-radius: 10px; height: 150px;'>
            <h4 style='color: #ffde59;'>🏭 Fábricas y Almacenes</h4>
            <p>Seguridad de trabajadores en áreas de riesgo</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Espacio para imagen de beneficios
    st.markdown("---")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(
            """
            <div style='background-color: #f8f9fa; 
                        padding: 20px; 
                        border-radius: 15px;
                        text-align: center;
                        height: 250px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        border: 2px dashed #27ae60;'>
            <p style='color: #27ae60;'>📈 Espacio para gráfico de beneficios</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            """
            <div style='background-color: #f8f9fa; 
                        padding: 20px; 
                        border-radius: 15px;
                        text-align: center;
                        height: 250px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        border: 2px dashed #27ae60;'>
            <p style='color: #27ae60;'>🏢 Espacio para imagen de instalación</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# ============================================
# PÁGINA: CÓMO FUNCIONA
# ============================================

elif page == "📱 Cómo Funciona":
    
    st.title("📱 Cómo Funciona AInomaly")
    
    # Explicación técnica simplificada
    st.markdown(
        """
        <div style='background-color: #2C3E50; color: white; padding: 30px; border-radius: 15px;'>
        <h3 style='color: white;'>🎯 Simple en 3 Pasos</h3>
        <ol style='font-size: 1.1rem;'>
        <li><strong>Conecta</strong>: Vincula AInomaly con tus cámaras existentes (RTSP, IP, o archivos)</li>
        <li><strong>Configura</strong>: Define zonas de monitoreo y tipos de alertas que necesitas</li>
        <li><strong>Protege</strong>: Recibe alertas instantáneas y monitorea desde cualquier lugar</li>
        </ol>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Demostración simulada
    st.markdown("---")
    st.markdown("### 🎬 Demostración Interactiva")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Selector de escenarios
        escenario = st.selectbox(
            "Selecciona un escenario de prueba:",
            ["Caída en pasillo", "Persona inconsciente", "Movimiento inusual", "Accidente laboral"]
        )
        
        # Botón de simulación
        if st.button("🚨 Simular Detección", use_container_width=True):
            st.success(f"✅ AInomaly ha detectado: {escenario}")
            st.info("📱 Alerta enviada al supervisor: 'Posible emergencia detectada en Zona A'")
        
        # Configuración simulada
        st.markdown("---")
        st.markdown("#### ⚙️ Configuración")
        
        zonas = st.multiselect(
            "Zonas a monitorear:",
            ["Entrada principal", "Pasillos", "Área común", "Habitaciones", "Cocina", "Baños"]
        )
        
        sensibilidad = st.slider("Sensibilidad de detección:", 1, 10, 7)
        
        if st.button("💾 Guardar Configuración", use_container_width=True):
            st.success("Configuración guardada exitosamente")
    
    with col2:
        # Área de visualización simulada
        st.markdown(
            """
            <div style='background-color: #000; 
                        padding: 20px; 
                        border-radius: 10px;
                        text-align: center;
                        height: 350px;
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        justify-content: center;
                        color: white;
                        position: relative;'>
            <div style='position: absolute; top: 20px; left: 20px; background-color: red; color: white; padding: 5px 10px; border-radius: 5px;'>
            EN VIVO
            </div>
            <p style='font-size: 1.2rem;'>🔴 Cámara 1 - Área Común</p>
            <div style='background-color: #333; width: 80%; height: 200px; border-radius: 5px; display: flex; align-items: center; justify-content: center; margin: 20px 0;'>
            <p>Vista previa de video en tiempo real</p>
            </div>
            <p>Estado: <span style='color: #2ecc71;'>● Monitoreando</span></p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Métricas simuladas
        col_met1, col_met2, col_met3 = st.columns(3)
        with col_met1:
            st.metric("Cámaras activas", "4", "+0")
        with col_met2:
            st.metric("Alertas hoy", "2", "-60%")
        with col_met3:
            st.metric("Tiempo respuesta", "45s", "-85%")

# ============================================
# PÁGINA: CONTACTO
# ============================================

elif page == "📞 Contacto":
    
    st.title("📞 Contáctanos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
            """
            <div style='background-color: #E8F4F8; padding: 30px; border-radius: 15px; height: 100%;'>
            <h3 style='color: #2C3E50;'>💬 ¿Listo para transformar tu seguridad?</h3>
            <p style='font-size: 1.1rem;'>
            AInomaly está listo para proteger a tus personas más vulnerables. 
            Agenda una demostración personalizada y descubre cómo podemos adaptar 
            la solución a tus necesidades específicas.
            </p>
            <hr>
            <h4>📧 Email</h4>
            <p>contacto@ainomaly.com</p>
            <h4>📞 Teléfono</h4>
            <p>+1 (800) 123-4567</p>
            <h4>🏢 Dirección</h4>
            <p>Av. Tecnología 123, Ciudad Digital</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        # Formulario de contacto
        st.markdown("### ✉️ Solicita una Demostración")
        
        with st.form("contact_form"):
            nombre = st.text_input("Nombre completo*")
            empresa = st.text_input("Empresa*")
            email = st.text_input("Email*")
            telefono = st.text_input("Teléfono")
            
            tipo_empresa = st.selectbox(
                "Tipo de empresa*",
                ["Selecciona...", "Hospital/Clínica", "Residencia de ancianos", 
                "Fábrica/Almacén", "Oficinas", "Otro"]
            )
            
            num_camaras = st.slider("Número aproximado de cámaras", 1, 100, 10)
            
            mensaje = st.text_area("¿Algo específico que quieras mencionar?", height=100)
            
            submitted = st.form_submit_button("📩 Enviar Solicitud", use_container_width=True)
            
            if submitted:
                if nombre and empresa and email and tipo_empresa != "Selecciona...":
                    st.success("✅ Solicitud enviada. Nos contactaremos en menos de 24 horas.")
                    st.balloons()
                else:
                    st.error("⚠️ Por favor completa los campos obligatorios (*)")
    
    # Testimonios (simulados)
    st.markdown("---")
    st.markdown("### 🌟 Lo que Dicen Nuestros Clientes")
    
    col_test1, col_test2, col_test3 = st.columns(3)
    
    with col_test1:
        st.markdown(
            """
            <div style='background-color: black; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);'>
            <p style='font-style: italic;'>"AInomaly detectó una caída en nuestra residencia y pudimos responder en 2 minutos. Salvó una vida."</p>
            <p><strong>María González</strong><br>Directora, Residencia La Paz</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col_test2:
        st.markdown(
            """
            <div style='background-color: black; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);'>
            <p style='font-style: italic;'>"La instalación fue sencilla y en una semana ya estábamos monitoreando. La reducción en costos de seguros ha sido notable."</p>
            <p><strong>Roberto Martínez</strong><br>Gerente, Almacenes Centrales</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col_test3:
        st.markdown(
            """
            <div style='background-color: black; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);'>
            <p style='font-style: italic;'>"La tranquilidad que da saber que tenemos este sistema es invaluable. Nuestros pacientes y sus familias están más seguros."</p>
            <p><strong>Dr. Carlos Ruiz</strong><br>Director Médico, Clínica Santa María</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# ============================================
# PIE DE PÁGINA
# ============================================


st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div style='text-align: center;'>
        <h5> AInomaly</h5>
        <p>Tu guardián digital inteligente</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div style='text-align: center;'>
        <p><strong>Transformando seguridad</strong><br>
        Una cámara a la vez</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div style='text-align: center;'>
        <p>© 2024 AInomaly Technologies</p>
        <p>Todos los derechos reservados</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Nota final
st.markdown(
    """
    <div style='text-align: center; margin-top: 20px; font-size: 0.8rem; color: #7f8c8d;'>
    <p>AInomaly está diseñado para aumentar la seguridad y bienestar. No reemplaza la supervisión humana directa cuando sea requerida.</p>
    </div>
    """,
    unsafe_allow_html=True
)
