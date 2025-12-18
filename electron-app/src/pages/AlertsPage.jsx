import React, { useState, useEffect } from 'react';
import { Bell, History, Settings, Send, Save, AlertTriangle, CheckCircle, Smartphone } from 'lucide-react';

const AlertsPage = () => {
    const [activeTab, setActiveTab] = useState('config'); // config, rules, history
    const [settings, setSettings] = useState({
        telegram_token: "",
        telegram_chat_id: "",
        enabled: false,
        min_duration: 2.0,
        cooldown: 60,
        attach_image: true
    });
    const [history, setHistory] = useState([]);
    const [statusMsg, setStatusMsg] = useState("");
    const [testing, setTesting] = useState(false);
    const [scanning, setScanning] = useState(false);
    const [discoveredUsers, setDiscoveredUsers] = useState([]);

    const fetchSettings = () => {
        fetch('http://127.0.0.1:8001/alerts/settings')
            .then(res => res.json())
            .then(data => setSettings(data))
            .catch(err => console.error("Error fetching settings:", err));
    };

    const fetchHistory = () => {
        fetch('http://127.0.0.1:8001/alerts/history')
            .then(res => res.json())
            .then(data => setHistory(data))
            .catch(err => console.error("Error fetching history:", err));
    };

    useEffect(() => {
        fetchSettings();
        if (activeTab === 'history') {
            fetchHistory();
        }
    }, [activeTab]);

    const handleSave = () => {
        setStatusMsg("Guardando...");
        fetch('http://127.0.0.1:8001/alerts/settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(settings)
        })
            .then(res => res.json())
            .then(() => setStatusMsg("Configuración guardada correctamente"))
            .catch(() => setStatusMsg("Error al guardar"));

        setTimeout(() => setStatusMsg(""), 3000);
    };

    const handleTest = () => {
        setTesting(true);
        setStatusMsg("Probando conexión...");

        fetch('http://127.0.0.1:8001/alerts/test', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                telegram_token: settings.telegram_token,
                telegram_chat_id: settings.telegram_chat_id
            })
        })
            .then(res => res.json())
            .then(data => {
                setStatusMsg(data.message);

                // Auto-fill Chat ID if found
                if (data.success && data.chat_id) {
                    setSettings(prev => ({ ...prev, telegram_chat_id: data.chat_id }));
                }

                setTesting(false);
            })
            .catch((e) => {
                console.error(e);
                setStatusMsg("Error de conexión");
                setTesting(false);
            });
    };

    const handleScanUsers = () => {
        setScanning(true);
        setStatusMsg("Buscando usuarios...");
        fetch('http://127.0.0.1:8001/alerts/discover', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ telegram_token: settings.telegram_token })
        })
            .then(res => res.json())
            .then(data => {
                setDiscoveredUsers(data);
                setStatusMsg(data.length > 0 ? `Se encontraron ${data.length} usuarios` : "No se encontraron usuarios recientes");
                setScanning(false);
            })
            .catch(() => {
                setStatusMsg("Error al buscar usuarios");
                setScanning(false);
            });
    };

    const handleFullTest = () => {
        if (!confirm("Esto enviará una alerta de prueba real a Telegram con una imagen simulada. ¿Continuar?")) return;

        setStatusMsg("Enviando alerta...");
        fetch('http://127.0.0.1:8001/alerts/test_full', { method: 'POST' })
            .then(res => res.json())
            .then(() => setStatusMsg("Alerta de prueba enviada"))
            .catch(() => setStatusMsg("Error al enviar prueba"));
    };

    return (
        <div className="space-y-6 animate-in fade-in duration-500 max-w-6xl mx-auto">
            <header className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold text-white mb-2 tracking-tight">Alertas y Notificaciones</h2>
                    <p className="text-slate-400">Configura el bot de Telegram y reglas de detección.</p>
                </div>
                {statusMsg && (
                    <div className="bg-blue-600/20 text-blue-400 px-4 py-2 rounded-lg text-sm font-medium border border-blue-500/30 animate-in slide-in-from-top-2">
                        {statusMsg}
                    </div>
                )}
            </header>

            {/* Tabs */}
            <div className="flex gap-4 border-b border-white/5 pb-1">
                <button
                    onClick={() => setActiveTab('config')}
                    className={`pb-3 px-4 text-sm font-medium transition-colors relative ${activeTab === 'config' ? 'text-blue-400' : 'text-slate-400 hover:text-white'}`}
                >
                    <div className="flex items-center gap-2">
                        <Smartphone size={18} /> Configuración
                    </div>
                    {activeTab === 'config' && <div className="absolute bottom-0 left-0 w-full h-0.5 bg-blue-500 rounded-t-full"></div>}
                </button>
                <button
                    onClick={() => setActiveTab('rules')}
                    className={`pb-3 px-4 text-sm font-medium transition-colors relative ${activeTab === 'rules' ? 'text-blue-400' : 'text-slate-400 hover:text-white'}`}
                >
                    <div className="flex items-center gap-2">
                        <Settings size={18} /> Reglas
                    </div>
                    {activeTab === 'rules' && <div className="absolute bottom-0 left-0 w-full h-0.5 bg-blue-500 rounded-t-full"></div>}
                </button>
                <button
                    onClick={() => setActiveTab('history')}
                    className={`pb-3 px-4 text-sm font-medium transition-colors relative ${activeTab === 'history' ? 'text-blue-400' : 'text-slate-400 hover:text-white'}`}
                >
                    <div className="flex items-center gap-2">
                        <History size={18} /> Historial
                    </div>
                    {activeTab === 'history' && <div className="absolute bottom-0 left-0 w-full h-0.5 bg-blue-500 rounded-t-full"></div>}
                </button>
            </div>

            {/* Content */}
            <div className="glass-panel p-6 rounded-2xl border-white/5">
                {activeTab === 'config' && (
                    <div className="space-y-6 max-w-3xl">
                        <div className="grid gap-6">
                            <div>
                                <label className="block text-sm font-medium text-slate-300 mb-2">Telegram Bot Token</label>
                                <input
                                    type="text"
                                    className="w-full bg-black/20 border border-white/10 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-blue-500 transition-colors font-mono text-sm"
                                    placeholder="123456789:ABCdefGHIjklMNOpqrsTUVwxYZ"
                                    value={settings.telegram_token}
                                    onChange={e => setSettings({ ...settings, telegram_token: e.target.value })}
                                />
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-slate-300 mb-2">Chat ID (Usuario o Grupo)</label>
                                <input
                                    type="text"
                                    className="w-full bg-black/20 border border-white/10 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-blue-500 transition-colors font-mono text-sm"
                                    placeholder="-1001234567890"
                                    value={settings.telegram_chat_id}
                                    onChange={e => setSettings({ ...settings, telegram_chat_id: e.target.value })}
                                />
                                <div className="mt-2">
                                    <button
                                        onClick={handleScanUsers}
                                        disabled={scanning || !settings.telegram_token}
                                        className="text-xs text-blue-400 hover:text-blue-300 font-medium flex items-center gap-1 mb-2 transition-colors"
                                    >
                                        {scanning ? "Buscando..." : "🔍 Buscar usuarios recientes (que escribieron al bot)"}
                                    </button>

                                    {discoveredUsers.length > 0 && (
                                        <div className="bg-slate-900/50 rounded-lg p-2 border border-white/5 space-y-1 max-h-40 overflow-y-auto animate-in fade-in slide-in-from-top-2">
                                            {discoveredUsers.map(u => (
                                                <button
                                                    key={u.id}
                                                    onClick={() => setSettings({ ...settings, telegram_chat_id: u.id })}
                                                    className="w-full text-left p-2 hover:bg-white/5 rounded-md flex justify-between items-center group transition-colors"
                                                >
                                                    <div>
                                                        <p className="text-sm text-slate-200 font-medium">{u.name}</p>
                                                        <p className="text-xs text-slate-500 uppercase tracking-wider text-[10px]">{u.type} • {u.id}</p>
                                                    </div>
                                                    {settings.telegram_chat_id === u.id && <CheckCircle size={16} className="text-emerald-500" />}
                                                </button>
                                            ))}
                                        </div>
                                    )}
                                </div>
                                <p className="text-xs text-slate-500 mt-1">Dejar vacío para auto-detectar o usar el buscador.</p>
                            </div>

                            <div className="flex items-center gap-3 p-4 bg-white/5 rounded-xl border border-white/5">
                                <button
                                    onClick={() => setSettings({ ...settings, enabled: !settings.enabled })}
                                    className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${settings.enabled ? 'bg-blue-600' : 'bg-slate-700'}`}
                                >
                                    <span className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${settings.enabled ? 'translate-x-6' : 'translate-x-1'}`} />
                                </button>
                                <span className="text-sm font-medium text-white">Activar Sistema de Alertas Global</span>
                            </div>
                        </div>

                        <div className="flex gap-4 pt-4 border-t border-white/5">
                            <button
                                onClick={handleSave}
                                className="flex items-center gap-2 px-6 py-2.5 bg-blue-600 hover:bg-blue-500 text-white rounded-lg font-medium transition-all shadow-lg shadow-blue-900/20 active:scale-95"
                            >
                                <Save size={18} /> Guardar Cambios
                            </button>
                            <button
                                onClick={handleTest}
                                disabled={testing}
                                className="flex items-center gap-2 px-6 py-2.5 bg-white/5 hover:bg-white/10 text-white rounded-lg font-medium transition-all border border-white/10"
                            >
                                <Send size={18} /> {testing ? "Probando..." : "Probar Conexión"}
                            </button>
                        </div>
                    </div>
                )}

                {activeTab === 'rules' && (
                    <div className="space-y-8 max-w-3xl">
                        <section>
                            <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                                <AlertTriangle size={20} className="text-amber-400" />
                                Detector de Caídas
                            </h3>
                            <div className="space-y-6 pl-2">
                                <div>
                                    <div className="flex justify-between mb-2">
                                        <label className="text-sm font-medium text-slate-300">Duración mínima de la caída (segundos)</label>
                                        <span className="text-blue-400 font-mono bg-blue-900/20 px-2 rounded">{settings.min_duration}s</span>
                                    </div>
                                    <input
                                        type="range"
                                        min="0.5" max="10" step="0.5"
                                        value={settings.min_duration}
                                        onChange={e => setSettings({ ...settings, min_duration: parseFloat(e.target.value) })}
                                        className="w-full accent-blue-500 h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer"
                                    />
                                    <p className="text-xs text-slate-500 mt-2">Tiempo que la persona debe permanecer detectada 'En el suelo' antes de alertar.</p>
                                </div>

                                <div>
                                    <div className="flex justify-between mb-2">
                                        <label className="text-sm font-medium text-slate-300">Cooldown por Cámara (segundos)</label>
                                        <span className="text-blue-400 font-mono bg-blue-900/20 px-2 rounded">{settings.cooldown}s</span>
                                    </div>
                                    <input
                                        type="range"
                                        min="10" max="300" step="10"
                                        value={settings.cooldown}
                                        onChange={e => setSettings({ ...settings, cooldown: parseInt(e.target.value) })}
                                        className="w-full accent-blue-500 h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer"
                                    />
                                    <p className="text-xs text-slate-500 mt-2">Tiempo de espera antes de enviar otra alerta desde la misma cámara.</p>
                                </div>
                            </div>
                        </section>

                        <section className="border-t border-white/5 pt-6">
                            <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                                <CheckCircle size={20} className="text-emerald-400" />
                                Contenido de la Alerta
                            </h3>
                            <div className="space-y-3">
                                <label className="flex items-center gap-3 p-3 bg-white/5 rounded-lg cursor-pointer hover:bg-white/10 transition">
                                    <input
                                        type="checkbox"
                                        checked={settings.attach_image}
                                        onChange={e => setSettings({ ...settings, attach_image: e.target.checked })}
                                        className="w-5 h-5 rounded border-slate-600 text-blue-600 focus:ring-blue-500 bg-slate-700"
                                    />
                                    <span className="text-slate-200">Adjuntar Snapshots (Imagen)</span>
                                </label>
                            </div>
                        </section>

                        <div className="flex gap-4 pt-6 border-t border-white/5">
                            <button
                                onClick={handleSave}
                                className="flex items-center gap-2 px-6 py-2.5 bg-blue-600 hover:bg-blue-500 text-white rounded-lg font-medium transition-all shadow-lg shadow-blue-900/20"
                            >
                                <Save size={18} /> Guardar Reglas
                            </button>
                            <button
                                onClick={handleFullTest}
                                className="flex items-center gap-2 px-6 py-2.5 bg-rose-600/20 hover:bg-rose-600/30 text-rose-400 rounded-lg font-medium transition-all border border-rose-500/20 ml-auto"
                            >
                                <Bell size={18} /> Simular Alerta Real
                            </button>
                        </div>
                    </div>
                )}

                {activeTab === 'history' && (
                    <div className="space-y-4">
                        <div className="flex justify-between items-center mb-4">
                            <p className="text-slate-400 text-sm">Mostrando últimas 100 alertas</p>
                            <button onClick={fetchHistory} className="text-blue-400 hover:text-blue-300 text-sm font-medium">Actualizar</button>
                        </div>
                        <div className="rounded-xl overflow-hidden border border-white/5">
                            <table className="w-full text-left">
                                <thead className="bg-white/5 text-slate-400 text-xs uppercase tracking-wider">
                                    <tr>
                                        <th className="p-4">Fecha</th>
                                        <th className="p-4">Cámara</th>
                                        <th className="p-4">Evento</th>
                                        <th className="p-4">Estado</th>
                                        <th className="p-4 text-right">Detalle</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-white/5">
                                    {history.length > 0 ? (
                                        history.map((alert, idx) => (
                                            <tr key={idx} className="hover:bg-white/5 transition-colors">
                                                <td className="p-4 text-slate-300 font-mono text-sm">{alert.date}</td>
                                                <td className="p-4 text-white font-medium">{alert.camera}</td>
                                                <td className="p-4">
                                                    <span className="px-2 py-1 rounded-md bg-rose-500/20 text-rose-400 text-xs font-bold border border-rose-500/20">
                                                        {alert.event}
                                                    </span>
                                                </td>
                                                <td className="p-4">
                                                    {alert.status === "Enviado" ? (
                                                        <span className="text-emerald-400 flex items-center gap-1.5 text-sm">
                                                            <CheckCircle size={14} /> Enviado
                                                        </span>
                                                    ) : (
                                                        <span className="text-slate-500 text-sm">{alert.status}</span>
                                                    )}
                                                </td>
                                                <td className="p-4 text-right text-slate-500 text-xs max-w-xs truncate">
                                                    {alert.details}
                                                </td>
                                            </tr>
                                        ))
                                    ) : (
                                        <tr>
                                            <td colSpan={5} className="p-8 text-center text-slate-500">
                                                No hay historial de alertas.
                                            </td>
                                        </tr>
                                    )}
                                </tbody>
                            </table>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default AlertsPage;
