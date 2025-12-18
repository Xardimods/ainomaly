# 📦 Guía de Instalación

Sigue estos pasos para configurar y ejecutar la aplicación **AInomaly** en una nueva máquina.

## Prerrequisitos

1.  **Python 3.10+**: [Descargar Aquí](https://www.python.org/downloads/)
    *   *Nota: Asegúrate de marcar "Add Python to PATH" durante la instalación.*
2.  **Node.js 18+**: [Descargar Aquí](https://nodejs.org/)

---

## 🚀 Instalación Rápida

### 1. Configurar Entorno Python
Abre una terminal (CMD o PowerShell) en la carpeta raíz del proyecto e instala las librerías necesarias:

```bash
pip install -r requirements.txt
```
*Esto instalará `ultralytics` (YOLO), `fastapi`, `opencv-python` y otras dependencias.*

### 2. Configurar Entorno Frontend
En la misma terminal, navega a la carpeta de la aplicación de escritorio e instala las dependencias de Node.js:

```bash
cd electron-app
npm install
```

---

## 🎮 Ejecución

Para iniciar el sistema completo (La aplicación abrirá automáticamente el backend de Python):

```bash
# Dentro de la carpeta electron-app
npm run electron
```

---

## 🛠️ Ejecución Manual (Modo Debug)

Si prefieres ejecutar los servicios por separado para ver los registros de error detallados:

1.  **Terminal 1 (Backend):**
    ```bash
    # Desde la raíz del proyecto
    python backend/api.py
    ```
    *Deberías ver `Uvicorn running on http://127.0.0.1:8001`*

2.  **Terminal 2 (Frontend):**
    ```bash
    # Desde la carpeta electron-app
    npm run dev
    ```

---

## ❓ Solución de Problemas

-   **"Module not found" en Python**: Asegúrate de haber instalado los `requirements.txt` en el entorno correcto.
-   **Cámara no visible**: Verifica que ninguna otra aplicación (como Zoom o Teams) esté usando la webcam.
-   **Políticas de Seguridad (PowerShell)**: Si `npm run electron` falla con un error de permisos en Windows, intenta ejecutar:
    ```cmd
    cmd /c npm run electron
    ```
-   **Modelo IA**: La primera vez que ejecutes el programa, se descargará automáticamente `yolov8n-pose.pt`. Si esto falla por conexión a internet, descárgalo manualmente y colócalo en `backend/models/`.
