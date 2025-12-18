# 📦 Installation Guide

Follow these steps to set up and run the application on a new machine.

## Prerequisites

1.  **Python 3.10+**: [Download Here](https://www.python.org/downloads/)
    *   *Note: Ensure you check "Add Python to PATH" during installation.*
2.  **Node.js 16+**: [Download Here](https://nodejs.org/)

---

## 🚀 Step 1: Backend Setup (Python)

Open a terminal (Command Prompt or PowerShell) and navigate to the project folder.

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *This will install YOLOv8 (`ultralytics`), FastAPI, OpenCV, and other required libraries.*

2.  **Start the Backend Server:**
    ```bash
    python backend/api.py
    ```
    *   You should see `Uvicorn running on http://127.0.0.1:8001`.
    *   **Keep this terminal open.**

---

## 💻 Step 2: Frontend Setup (Electron)

Open a **new** terminal window and navigate to the `electron-app` folder.

```bash
cd electron-app
```

1.  **Install Dependencies (First time only):**
    ```bash
    npm install
    ```

2.  **Run the App:**
    ```bash
    npm run electron
    ```

---

## 🛠️ Troubleshooting

-   **"Module not found" in Python**: Ensure you installed the requirements in the correct environment.
-   **Camera not showing**: Check if another app is using the webcam.
-   **Security Policies (Windows)**: If `npm run electron` fails with a security error, try running:
    ```cmd
    cmd /c npm run electron
    ```
