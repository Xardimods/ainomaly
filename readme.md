# AInomaly

### _Sistema de Videoreconocimiento de Anomalías en Tiempo Real_

**AInomaly** es una plataforma de seguridad avanzada que utiliza Inteligencia Artificial para detectar caídas y anomalías a través de cámaras de seguridad (RTSP) o webcams. Combina un potente backend en Python con una moderna interfaz de escritorio en Electron.

---

### Arquitectura del Sistema

El proyecto se divide en dos módulos principales que se comunican entre sí:

1.  **Backend (Python/FastAPI):**

    - **The Eye (Visión):** Procesamiento de video en tiempo real utilizando **YOLOv8-Pose**.
    - **The Brain (Lógica):** Análisis de vectores esqueléticos para detectar caídas con alta precisión.
    - **The Messenger (Alertas):** Gestión de notificaciones, bot de Telegram y almacenamiento de eventos.
    - **Stream Server:** Servidor RSTP/MJPEG optimizado para transmitir video procesado al frontend.

2.  **Frontend (Electron + React):**
    - **Interfaz de Usuario:** Dashboard moderno con soporte para modo oscuro.
    - **Configuración:** Gestión de cámaras, zonas de detección y sensibilidad.
    - **Historial:** Visualización de alertas pasadas y grabaciones de evidencia.
    - **Control:** Inicio y parada automática del motor de IA.

---

### Estructura del Proyecto

```
ainomaly/
├── backend/               # Código fuente del servidor Python
│   ├── api.py            # Punto de entrada FastAPI
│   ├── models/           # Pesos del modelo (yolov8n-pose.pt)
│   ├── source/           # Lógica de visión y detección
│   └── ...
├── electron-app/          # Aplicación de Escritorio (React)
│   ├── src/              # Componentes y páginas
│   ├── main.cjs          # Proceso principal de Electron
│   └── ...
├── scripts/               # Scripts de utilidad y depuración
├── recordings/            # Videoclips de eventos detectados
├── snapshots/             # Fotos de evidencia
└── actions...
```

---

### Tecnologías

- **IA / Visión:** YOLOv8, OpenCV, NumPy
- **Backend:** FastAPI, Uvicorn
- **Frontend:** Electron, React, TailwindCSS
- **Notificaciones:** Telegram Bot API
- **Hardware:** Soporte para CPU (optimizado) y GPU (CUDA opcional)

---

### Instalación y Ejecución

#### Prerrequisitos

- **Python 3.10+**
- **Node.js 18+**

#### 1. Configuración del Entorno Python

Instala las dependencias del backend en la raíz del proyecto:

```bash
pip install -r requirements.txt
```

#### 2. Configuración del Frontend

Instala las dependencias de Node.js dentro de la carpeta `electron-app`:

```bash
cd electron-app
npm install
```

#### 3. Ejecutar la Aplicación

Para iniciar el sistema completo (Frontend + Backend automático):

```bash
# Desde la carpeta electron-app
npm run electron
```

El backend de Python se iniciará automáticamente en segundo plano cuando la aplicación de escritorio se abra.

---

### 📝 Notas

- El modelo `yolov8n-pose.pt` se descargará automáticamente si no está presente en `backend/models/`.
- Asegúrate de tener configurada una cámara válida (Webcam índice 0 o URL RTSP) en la configuración para ver video en vivo.
