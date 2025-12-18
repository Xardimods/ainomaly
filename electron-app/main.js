import { app, BrowserWindow } from 'electron';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
import { spawn } from 'child_process';

let backendProcess = null;

const startBackend = () => {
    const rootDir = path.join(__dirname, '..');
    console.log("Starting Python Backend from:", rootDir);

    // Spawn python process
    // Assumes 'python' is in PATH. On some systems might be 'python3'
    backendProcess = spawn('python', ['backend/api.py'], {
        cwd: rootDir,
        stdio: 'inherit', // Pipe output to console for debugging
        shell: true       // fast way to ensure it runs in shell context if needed
    });

    backendProcess.on('error', (err) => {
        console.error("Failed to start backend:", err);
    });

    backendProcess.on('exit', (code, signal) => {
        console.log(`Backend exited with code ${code} and signal ${signal}`);
    });
};

const killBackend = () => {
    if (backendProcess) {
        console.log("Killing backend process...");
        // On Windows with shell:true, we might need a tree kill, but usually standard kill works for simple cases
        // or using 'taskkill' if needed. For now standard:
        backendProcess.kill();
        backendProcess = null;
    }
};

function createWindow() {
    const win = new BrowserWindow({
        width: 1280,
        height: 720,
        minWidth: 1024,
        minHeight: 600,
        webPreferences: {
            preload: path.join(__dirname, 'preload.cjs'),
            nodeIntegration: false,
            contextIsolation: true,
        },
        // Dark theme frame
        backgroundColor: '#1a1a1a',
        titleBarStyle: 'hidden',
        titleBarOverlay: {
            color: '#1a1a1a',
            symbolColor: '#ffffff',
            height: 30
        }
    });

    // In production, load the build file.
    // In development, load the vite dev server url.
    const isDev = !app.isPackaged;

    if (isDev) {
        win.loadURL('http://localhost:5173');
        win.webContents.openDevTools();
    } else {
        // win.loadFile(path.join(__dirname, 'dist/index.html'));
        // For now we focus on dev mode
        console.log("Production build not yet configured");
    }
}

app.whenReady().then(() => {
    startBackend();
    createWindow();

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
});

app.on('window-all-closed', () => {
    killBackend();
    if (process.platform !== 'darwin') {
        app.quit();
    }
});
