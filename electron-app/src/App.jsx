import React from 'react';
import { HashRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import MediaPage from './pages/MediaPage';

import Settings from './pages/Settings';
import Cameras from './pages/Cameras';
import AlertsPage from './pages/AlertsPage';

import { AlertTriangle, X } from 'lucide-react';

const NotificationOverlay = () => {
  const [notification, setNotification] = React.useState(null);

  React.useEffect(() => {
    // Request desktop notification permission
    if (Notification.permission !== 'granted') {
      Notification.requestPermission();
    }

    const eventSource = new EventSource('http://127.0.0.1:8001/events');

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'alert') {
          // 1. In-App Notification
          setNotification(data);
          setTimeout(() => setNotification(null), (data.duration || 5) * 1000);

          // 2. Native Desktop Notification
          if (Notification.permission === 'granted') {
            new Notification("🚨 AInomaly Alert", {
              body: `${data.message} en ${data.camera}`,
              icon: '/favicon.ico'
            });
          }
        }
      } catch (e) {
        console.error("Error parsing SSE", e);
      }
    };

    return () => {
      eventSource.close();
    };
  }, []);

  if (!notification) return null;

  return (
    <div className="fixed top-8 left-1/2 transform -translate-x-1/2 z-50 animate-in slide-in-from-top-4 fade-in duration-300">
      <div className="bg-rose-600/90 backdrop-blur-md text-white px-6 py-4 rounded-xl shadow-2xl border border-rose-400/30 flex items-center gap-4 max-w-md w-full">
        <div className="bg-white/20 p-2 rounded-full animate-pulse">
          <AlertTriangle size={24} className="text-white" />
        </div>
        <div>
          <h3 className="font-bold text-lg">{notification.message || "Caída Detectada"}</h3>
          <p className="text-rose-100 text-sm">{notification.camera} • {new Date().toLocaleTimeString()}</p>
        </div>
        <button onClick={() => setNotification(null)} className="ml-auto text-white/60 hover:text-white">
          <X size={20} />
        </button>
      </div>
    </div>
  );
};

function App() {
  return (
    <Router>
      <div className="flex h-screen">
        <NotificationOverlay />
        <Sidebar />
        <main className="flex-1 overflow-auto p-8 relative">
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/cameras" element={<Cameras />} />
            <Route path="/alerts" element={<AlertsPage />} />
            <Route path="/media" element={<MediaPage />} />

            <Route path="/settings" element={<Settings />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
