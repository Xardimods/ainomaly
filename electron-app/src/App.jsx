import React from 'react';
import { HashRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import Rankings from './pages/Recordings'; // Mapped 'Grabaciones' to Recordings
import CameraTest from './pages/CameraTest';
import Settings from './pages/Settings';

function App() {
  return (
    <Router>
      <div className="flex h-screen">
        <Sidebar />
        <main className="flex-1 overflow-auto p-8 relative">
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/recordings" element={<Rankings />} />
            <Route path="/files" element={<div className="p-10">Archivos (In Construction)</div>} />
            <Route path="/camera-test" element={<CameraTest />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
