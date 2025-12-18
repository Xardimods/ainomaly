const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let backendProcess = null;

const startBackend = () => {
  let scriptPath;
  let cwd;

  if (app.isPackaged) {
    // In production, resources are unpacked in "resources" folder
    cwd = process.resourcesPath;
    scriptPath = path.join(process.resourcesPath, 'backend', 'api.py');
  } else {
    // In development, we are in electron-app/ folder
    cwd = path.join(__dirname, '..');
    scriptPath = 'backend/api.py';
  }

  console.log("Starting Python Backend from:", cwd);
  console.log("Script:", scriptPath);

  // Spawn python process
  // We assume 'python' is in the system PATH as per INSTALL.md requirements
  const pythonCmd = 'python';

  backendProcess = spawn(pythonCmd, [scriptPath], {
    cwd: cwd,
    stdio: 'inherit',
    shell: true
  });

  backendProcess.on('error', (err) => {
    console.error("Failed to start backend:", err);
  });

  backendProcess.on('exit', (code, signal) => {
    console.log(`Backend exited with code ${code} and signal ${signal}`);
    backendProcess = null;
  });
};

const killBackend = () => {
  if (backendProcess) {
    console.log("Killing backend process...");
    // Force kill if necessary - simple kill is safer for now
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
    backgroundColor: '#1a1a1a',
    titleBarStyle: 'hidden',
    titleBarOverlay: {
      color: '#1a1a1a',
      symbolColor: '#ffffff',
      height: 30
    }
  });

  const isDev = !app.isPackaged;

  if (isDev) {
    win.loadURL('http://localhost:5173');
  } else {
    win.loadFile(path.join(__dirname, 'dist/index.html'));
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
