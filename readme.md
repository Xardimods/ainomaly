# 🛡️ AInomaly

### _Detector Inteligente de Anomalías y Caídas_

**AInomaly** es un sistema de seguridad automatizado que transforma una cámara estándar en un sensor inteligente. Utilizando visión por computadora y heurística geométrica, el sistema detecta caídas y comportamientos anómalos en tiempo real para enviar alertas inmediatas.

---

### 🚀 Arquitectura del Sistema

El proyecto integra cuatro módulos principales operando en simultáneo:

1.  **👁️ The Eye (Visión):** Captura video y extrae el esqueleto humano mediante **MediaPipe**.
2.  **🧠 The Brain (Lógica):** Analiza vectores y ángulos para diferenciar una actividad normal de una caída crítica.
3.  **🔔 The Messenger (IoT):** Envía notificaciones push y evidencia fotográfica a través de un **Bot de Telegram**.
4.  **🖥️ The Face (Interfaz):** Dashboard interactivo en **Streamlit** para monitoreo en vivo.

---

### ✨ Características Clave

- **Detección en Tiempo Real:** Procesamiento inmediato de frames de video.
- **Privacidad:** El análisis ocurre localmente; solo se transmiten las alertas.
- **Lógica Geométrica:** Alta precisión sin necesidad de entrenar redes neuronales pesadas (Black Boxes).
- **Alertas Remotas:** Conexión directa al móvil del cuidador.

---

### 🛠️ Tecnologías

- **Lenguaje:** Python 3.x
- **Visión:** OpenCV, MediaPipe Pose
- **Comunicación:** Requests, Python-Telegram-Bot
- **Frontend:** Streamlit

---

### 🚦 Instalación Rápida

1.  **Instalar dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Configurar variables:**
    Crea un archivo `.env` con tus credenciales (Token de Telegram y Chat ID).

3.  **Ejecutar AInomaly:**
    ```bash
    streamlit run main.py
    ```
